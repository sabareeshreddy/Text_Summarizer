from flask import Flask, jsonify, request, Blueprint, send_from_directory
from werkzeug.utils import secure_filename
from src.components.extraction import extract
from src.components import summarizer
from datetime import datetime
import time
import os
from scripts.hashcal import hash_file

summarize_bp = Blueprint("summarize", __name__, url_prefix="/summarize")


@summarize_bp.route("/", methods=["GET"])
def summarize():
    type = request.args.get("type")
    link = request.args.get("link")
    current_time = datetime.now()
    start_time = time.time()
    data = extract(int(type), link)
    extraction_time = time.time() - start_time
    result = summarizer.summarize(data)
    summarizer_time = time.time() - start_time - extraction_time
    result["start_time"] = current_time
    result["extraction_time"] = round(extraction_time, 3)
    result["summarizer_time"] = round(summarizer_time, 3)
    return jsonify(result)
