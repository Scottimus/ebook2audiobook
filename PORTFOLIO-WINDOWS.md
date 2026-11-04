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

The compatibility pins reproduce an older environment and are not a general upgrade recommendation. Test them on your target Python/GPU combination. A fresh end-to-end model conversion is tracked separately from the mocked regression checks.

The conversion engine, UI, and model integrations originate in [DrewThomasson/ebook2audiobook](https://github.com/DrewThomasson/ebook2audiobook). The original Apache license and upstream history are retained.
