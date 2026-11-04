"""Exercise local speech export using a short original text and an existing XTTS model."""
import argparse
from pathlib import Path
import wave


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text", type=Path)
    parser.add_argument("--model-dir", required=True, type=Path)
    parser.add_argument("--reference", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Choose a new output filename")
    text = args.text.read_text(encoding="utf-8").strip()
    if not text or len(text) > 1000:
        parser.error("The smoke-test text must contain 1–1000 characters")
    from TTS.api import TTS
    model = TTS(model_path=str(args.model_dir), config_path=str(args.model_dir / "config.json")).to(args.device)
    model.tts_to_file(text=text, speaker_wav=str(args.reference), language="en", file_path=str(args.output))
    with wave.open(str(args.output)) as audio:
        if audio.getnframes() == 0:
            raise RuntimeError("Generated audio is empty")
        print(f"Saved to: {args.output}; {audio.getnframes() / audio.getframerate():.2f} seconds")


if __name__ == "__main__":
    main()
