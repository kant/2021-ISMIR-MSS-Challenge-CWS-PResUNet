from predictor import SubbandResUNetPredictor
import time
import os
from argparse import ArgumentParser
from progressbar import *

parser = ArgumentParser()

parser.add_argument("-i", "--input_file_path", default="", help="The .wav file or the audio folder to be processed")
parser.add_argument("-o", "--output_path", default="", help="The output dirpath for the results")
parser.add_argument("--cuda", nargs="?",default="", help="Whether use GPU acceleration.")

args = parser.parse_args()

if __name__ == '__main__':
    scaledmixture_predictor = SubbandResUNetPredictor(cuda=True if(args.cuda is None) else False)

    submission = scaledmixture_predictor
    submission.prediction_setup()

    if(not os.path.isdir(args.input_file_path)):
        assert args.input_file_path[-3:] == "wav" or args.input_file_path[-4:] == "flac", \
            "Error: invalid file " + args.input_file_path + ", we only accept .wav and .flac file."
        output_path = os.path.join(args.output_path,os.path.splitext(os.path.basename(args.input_file_path))[0])
        if(not os.path.exists(output_path)):
            os.makedirs(output_path, exist_ok=True)

        bass = os.path.join(output_path,"bass.wav")
        vocals = os.path.join(output_path,"vocals.wav")
        drums = os.path.join(output_path,"drums.wav")
        other = os.path.join(output_path,"other.wav")
        submission.prediction(
            mixture_file_path=args.input_file_path,
            vocals_file_path=vocals, bass_file_path=bass, drums_file_path=drums, other_file_path=other)
    else:
        files = os.listdir(args.input_file_path)
        print("Found", len(files), "files in", args.input_file_path)
        widgets = [
            "Performing Separation",
            ' [', Timer(), '] ',
            Bar(),
            ' (', ETA(), ') ',
        ]
        pbar = ProgressBar(widgets=widgets).start()

        for i, file in enumerate(files):
            if(not file[-3:] == "wav" and not file[-4:] == "flac"):
                print("Ignore file",file," unsupported file type. Please use wav or flac format.")
            output_path = os.path.join(args.output_path, os.path.splitext(os.path.basename(file))[0])
            if (not os.path.exists(output_path)):
                os.makedirs(output_path, exist_ok=True)
            bass = os.path.join(output_path, "bass.wav")
            vocals = os.path.join(output_path, "vocals.wav")
            drums = os.path.join(output_path, "drums.wav")
            other = os.path.join(output_path, "other.wav")
            submission.prediction(
                mixture_file_path=os.path.join(args.input_file_path,file),
                vocals_file_path=vocals, bass_file_path=bass, drums_file_path=drums, other_file_path=other)
            pbar.update(int((i / (len(files) - 1)) * 100))

    print("Prediction Success")
