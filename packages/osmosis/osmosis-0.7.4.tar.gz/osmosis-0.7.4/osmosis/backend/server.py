from flask import Flask, send_from_directory
from flask_socketio import SocketIO
import eventlet

from osmosis.frontend import dist as frontend

from osmosis.backend.model import OsmosisModel
from osmosis.backend.config import Config
from osmosis.backend.fs import (
    save_image,
    delete_image,
    read_image_metadata,
    load_models,
    save_models,
)

from rich import print

import diffusers

from uuid import uuid4
import os
import sys
import platform
import packaging.version as semver


class OsmosisServer:
    def __init__(self, port: int):
        self.port = port
        self.app = Flask(
            __name__, static_url_path="", static_folder=frontend.__path__[0]
        )
        self.sio = SocketIO(self.app)

        self.model = OsmosisModel(sio=self.sio)

        if not Config.DEBUG:
            diffusers.logging.set_verbosity_error()
        else:
            diffusers.logging.set_verbosity_info()

        self.register_routes()
        self.register_ws_handlers()

    def register_routes(self):
        @self.app.route("/")
        def serve_index():
            return send_from_directory(self.app.static_folder, "index.html")

        @self.app.route("/outputs/<path:name>")
        def serve_outputs(name):
            return send_from_directory(Config.OUTPUTS_DIR, name)

    def register_ws_handlers(self):
        @self.sio.on("info")
        def info():
            coreml_available = False
            if platform.system() == "Darwin":
                macos_version = semver.parse(platform.mac_ver()[0])
                coreml_available = macos_version >= semver.parse("13.1")

            return {
                "model": {"type": self.model.type, "name": self.model.name},
                "models": load_models(),
                "coreml_available": coreml_available,
            }

        @self.sio.on("load_model")
        def load_model(model_internal_id):
            print(f"Loading model {model_internal_id}")

            models = load_models()
            model = models.get(model_internal_id, None)

            if not model:
                print(f"Unknown model {model_internal_id}", file=sys.stderr)
                return

            if model["type"] == "diffusers":
                self.model.load_diffusers(
                    model["id"],
                    revision=model.get("revision", "main"),
                    half=model.get("half", False),
                )
            elif model["type"] == "coreml":
                self.model.load_coreml(model["path"], model["mlpackages"])
            elif model["type"] == "checkpoint":
                self.model.load_checkpoint(model["path"], half=model.get("half", False))
            else:
                raise NotImplementedError()

            print(f"[green]Loaded model {model_internal_id}[/green]")

        @self.sio.on("add_model")
        def add_model(data: dict):
            model_type = data.get("model_type", "diffusers")

            new_internal_id = uuid4().hex

            if model_type == "diffusers":
                model_id = data.get("model_id", None)
                revision = data.get("revision", None)
                half = data.get("half", False)

                prev_models = load_models()
                prev_models[new_internal_id] = {
                    "type": "diffusers",
                    "id": model_id,
                    "half": half,
                }

                if revision:
                    prev_models[new_internal_id]["revision"] = revision

                save_models(prev_models)
            elif model_type == "coreml":
                model_id = data["model_id"]
                mlpackages_dir = data["mlpackages_dir"]

                prev_models = load_models()
                prev_models[new_internal_id] = {
                    "type": "coreml",
                    "path": model_id,
                    "mlpackages": mlpackages_dir,
                }
                save_models(prev_models)
            elif model_type == "checkpoint":
                path = data["path"]
                half = data.get("half", False)

                prev_models = load_models()
                prev_models[new_internal_id] = {
                    "type": "checkpoint",
                    "path": path,
                    "half": half,
                }
                save_models(prev_models)
            else:
                raise NotImplementedError()

        @self.sio.on("txt2img")
        def txt2img(data):
            print(data)
            output = self.model.txt2img(data)

            if output:
                save_image(output["image"], output["metadata"])

            self.sio.emit("txt2img:done")
            eventlet.sleep(0)

        @self.sio.on("gallery")
        def gallery():
            files = [
                name for name in os.listdir(Config.OUTPUTS_DIR) if name.endswith(".png")
            ]

            files.sort(
                key=lambda x: os.path.getmtime(os.path.join(Config.OUTPUTS_DIR, x))
            )
            files.reverse()

            return {"files": files}

        @self.sio.on("gallery:delete")
        def gallery_delete(name: str):
            delete_image(name)

        @self.sio.on("gallery:metadata")
        def gallery_metadata(name: str):
            if name == None:
                return None
            return read_image_metadata(name)

    def start(self):
        print(f"Osmosis started on [blue]http://localhost:{self.port}/[/blue]")

        self.sio.run(self.app, port=self.port, debug=Config.DEBUG)
