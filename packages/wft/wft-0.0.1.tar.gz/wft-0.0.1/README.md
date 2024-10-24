# wft

## Prepare dataset

```py
outdir = "output"
ft = (
    WhisperFineTuner(outdir)
    .prepare_dataset(
        "mozilla-foundation/common_voice_16_1",
        src_subset="zh-TW",
        src_audio_column="audio",
        src_transcription_column="sentence",
    )
    .push_dataset("JacobLinCool/mozilla-foundation-common_voice_16_1-zh-TW-preprocessed")
)
```

## Fine-tune

```py
outdir = "output"
ft = (
    WhisperFineTuner(outdir)
    .set_baseline("openai/whisper-large-v3-turbo", language="zh", task="transcribe")
    .then(lambda ft: print(ft.baseline_model))
    .load_dataset(
        "JacobLinCool/mozilla-foundation-common_voice_16_1-zh-TW-preprocessed"
    )
    .then(lambda ft: print(ft.dataset))
    .set_metric("cer")
    .set_lora_config() # use default config. see ft.default_lora_config for details
    .train() # use default config. see ft.default_training_args for details
    .merge_and_save(f"{outdir}/merged_model")
)
```

## Chaining All Together

```py
outdir = "output"
ft = (
    WhisperFineTuner(outdir)
    .prepare_dataset(
        "mozilla-foundation/common_voice_16_1",
        src_subset="zh-TW",
        src_audio_column="audio",
        src_transcription_column="sentence",
    )
    .set_baseline("openai/whisper-large-v3-turbo", language="zh", task="transcribe")
    .set_metric("cer")
    .set_lora_config() # use default config. see ft.default_lora_config for details
    .train() # use default config. see ft.default_training_args for details
    .merge_and_save(f"{outdir}/merged_model")
)
```
