import lsl_perun32 as lsl
import EKGProcessor as ekgp
import EKGapp as ekgapp
import argparse
import test_signal as ts

def run_online(chunk_size, Fs, channel):
    # Start the LSL stream
    inlet = lsl.start_stream('stream_1')

    # Create the processor, peaks detector and HRV analyzer
    processor = ekgp.SignalProcessor(inlet=inlet, samps_per_chunk=chunk_size, sampling_rate=Fs, buffor_size_seconds=5, mode='online', channel=channel)
    peaks_detector =  ekgp.PeaksDetector(processor)
    hrv_analyzer = ekgp.HRVAnalyzer(peaks_detector)

    # Run the application
    ekgapp.run_dash_app_thread(processor, peaks_detector, hrv_analyzer)

def run_offline(chunk_size, Fs, s_path, n_ch, channel, channel_base):
    # Generate the test signal
    inlet = ts.test_signal(s_path=s_path, n_ch=n_ch, dtype='<f', channel=channel, channel_base=channel_base, fs=Fs, chunk_size=chunk_size)

    # Create the processor, peaks detector and HRV analyzer
    processor = ekgp.SignalProcessor(inlet=inlet, samps_per_chunk=chunk_size, sampling_rate=Fs, buffor_size_seconds=5, mode='offline')
    peaks_detector = ekgp.PeaksDetector(processor)
    hrv_analyzer = ekgp.HRVAnalyzer(peaks_detector)

    # Run the application
    ekgapp.run_dash_app_thread(processor, peaks_detector, hrv_analyzer)

def main():
    # Parse the arguments
    parser = argparse.ArgumentParser(description="EKG Processor Application")

    parser.add_argument('--mode', choices=['online', 'offline'], required=True, help="Mode to run the application in")
    parser.add_argument('--chunk_size', type=int, default=16, help="Chunk size for signal processing")
    parser.add_argument('--Fs', type=int, default=500, help="Sampling frequency")
    parser.add_argument('--n_ch', type=int, default=1, help="Channel count")
    parser.add_argument('--channel', type=int, default=0, help="Channel number")
    parser.add_argument('--channel_base', type=int, default=-1, help="Base channel number")
    parser.add_argument('--s_path', type=str, default='test_perun.raw', help="Signal path for offline mode")

    args = parser.parse_args()

    # Run the application in the selected mode
    if args.mode == 'online':
        run_online(args.chunk_size, args.Fs, args.channel)
    elif args.mode == 'offline':
        run_offline(args.chunk_size, args.Fs, args.s_path, args.n_ch, args.channel, args.channel_base)
    else:
        print("Invalid mode selected. Use 'online' or 'offline'.")

if __name__ == '__main__':
    main()