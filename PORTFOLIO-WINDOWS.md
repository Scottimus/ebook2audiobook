# Windows compatibility example

This attributed fork preserves the audited upstream snapshot and adds focused local compatibility work.

- Scan PATH directories for shared FFmpeg DLLs and deduplicate candidates.
- Keep the older speech dependency family together for the previously used CUDA environment.
- Show the finished audiobook path in completion feedback and preserve output state after session reset for single and directory jobs.
- Handle an empty export list and remove a success-path reference to an undefined session diagnostic variable.

```sh
python -m unittest discover -s tests -p test_windows_export.py -v
```

The tests execute the actual finalization function with mocked synthesis, export, and session services. They verify both completion paths and empty output. They require only Python's standard library. Full ebook conversion additionally requires the upstream application dependencies, system tools, and a speech model. Follow the upstream README and model terms for those components.

## Local speech smoke test

`examples/local_speech_smoke.py` exercises the model/audio-export portion with an original short text. Its separate runtime was verified with Python 3.10, coqui-tts 0.24.3, PyTorch 2.5.1 CUDA 11.8, and transformers 4.46.2.

```sh
python examples/local_speech_smoke.py examples/short-original.txt --model-dir MODEL_DIRECTORY --reference reference.wav --output new-sample.wav
```

Use `--device cuda` for a compatible GPU. This small test isolates local speech export. The upstream application's full EPUB parsing, chapter assembly, and UI pipeline require their own complete environment and end-to-end validation.

The compatibility pins reproduce an older environment and are not a general upgrade recommendation. Test them on your target Python/GPU combination. A fresh end-to-end model conversion is tracked separately from the mocked regression checks.

The conversion engine, UI, and model integrations originate in [DrewThomasson/ebook2audiobook](https://github.com/DrewThomasson/ebook2audiobook). The original Apache license and upstream history are retained.
