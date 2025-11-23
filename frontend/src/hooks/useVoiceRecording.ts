import { useState, useCallback, useRef } from 'react';
import { audioRecorder } from '../services/audioRecorder';

export const useVoiceRecording = () => {
    const [isRecording, setIsRecording] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const audioRef = useRef<Blob | null>(null);

    const startRecording = useCallback(async () => {
        try {
            setError(null);
            await audioRecorder.startRecording();
            setIsRecording(true);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to start recording');
            setIsRecording(false);
        }
    }, []);

    const stopRecording = useCallback(async (): Promise<Blob | null> => {
        try {
            const blob = await audioRecorder.stopRecording();
            audioRef.current = blob;
            setIsRecording(false);
            return blob;
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to stop recording');
            setIsRecording(false);
            return null;
        }
    }, []);

    const getAudioBlob = useCallback(() => audioRef.current, []);

    return {
        isRecording,
        error,
        startRecording,
        stopRecording,
        getAudioBlob,
    };
};
