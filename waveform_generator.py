import os, json, librosa, numpy as np, matplotlib.pyplot as plt, soundfile as sf

# This script uses the audio analysis peaks to generate simple waveform PNGs.
# IMPORTANT: This generator requires local audio files if you want full waveforms.
# For tracks with no local audio, it will attempt to use analysis segments to create a proxy waveform.

os.makedirs('output/waveforms', exist_ok=True)

ana_path = 'output/audio_analysis.json'
if not os.path.exists(ana_path):
    print('audio_analysis not found; waveform generator will produce proxy images based on segments.')
    analyses = {}
else:
    with open(ana_path) as f:
        analyses = json.load(f)

# Create a proxy waveform using segments' timbre or loudness where full audio is not available
for tid, analysis in analyses.items():
    try:
        # Prefer segments if available
        segments = analysis.get('segments',[])
        if segments:
            values = [s.get('loudness_max', -60.0) for s in segments]
            times = np.linspace(0, len(values), num=len(values))
            plt.figure(figsize=(10,2.5))
            plt.plot(times, values)
            plt.title(f'Proxy waveform for {tid}')
            plt.ylabel('loudness_max')
            plt.tight_layout()
            out = f'output/waveforms/{tid}.png'
            plt.savefig(out)
            plt.close()
        else:
            # fallback blank image
            plt.figure(figsize=(10,2.5))
            plt.text(0.5,0.5,'No segments available',ha='center',va='center')
            plt.axis('off')
            out = f'output/waveforms/{tid}.png'
            plt.savefig(out)
            plt.close()
    except Exception as e:
        print('waveform gen failed for', tid, e)
print('Generated waveform PNGs (proxy).')