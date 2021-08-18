import nemo.collections.asr as nemo_asr
wave_file = ['test.wav']
quartznet = nemo_asr.models.EncDecCTCModel.from_pretrained(model_name="QuartzNet15x5Base-En")
quartznet.transcribe(paths2audio_files=wave_file)
