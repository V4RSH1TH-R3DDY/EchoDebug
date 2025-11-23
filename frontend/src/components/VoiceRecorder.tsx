import React, { useState } from 'react';
import { useVoiceRecording } from '../hooks/useVoiceRecording';
import { apiClient } from '../services/apiClient';
import './VoiceRecorder.css';

interface VoiceRecorderProps {
    onTranscription: (text: string) => void;
    onError: (error: string) => void;
}

export const VoiceRecorder: React.FC<VoiceRecorderProps> = ({ onTranscription, onError }) => {
    const { isRecording, error, startRecording, stopRecording } = useVoiceRecording();
    const [isProcessing, setIsProcessing] = useState(false);

    const handleMouseDown = async () => {
        if (!isRecording && !isProcessing) {
            await startRecording();
        }
    };

    const handleMouseUp = async () => {
        if (isRecording) {
            setIsProcessing(true);
            const audioBlob = await stopRecording();

            if (audioBlob) {
                try {
                    const result = await apiClient.transcribeAudio(audioBlob);
                    onTranscription(result.text);
                } catch (err) {
                    onError(err instanceof Error ? err.message : 'Transcription failed');
                }
            }

            setIsProcessing(false);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.code === 'Space' && !e.repeat) {
            e.preventDefault();
            handleMouseDown();
        }
    };

    const handleKeyUp = (e: React.KeyboardEvent) => {
        if (e.code === 'Space') {
            e.preventDefault();
            handleMouseUp();
        }
    };

    return (
        <div className="voice-recorder">
            <button
                className={`record-button ${isRecording ? 'recording' : ''} ${isProcessing ? 'processing' : ''}`}
                onMouseDown={handleMouseDown}
                onMouseUp={handleMouseUp}
                onMouseLeave={handleMouseUp}
                onKeyDown={handleKeyDown}
                onKeyUp={handleKeyUp}
                disabled={isProcessing}
                aria-label="Push to talk"
            >
                <div className="record-button-inner">
                    {isProcessing ? (
                        <div className="spinner" />
                    ) : (
                        <>
                            <svg
                                className="microphone-icon"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="2"
                            >
                                <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" />
                                <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
                                <line x1="12" y1="19" x2="12" y2="23" />
                                <line x1="8" y1="23" x2="16" y2="23" />
                            </svg>
                            {isRecording && (
                                <div className="recording-pulse">
                                    <div className="pulse-ring" />
                                    <div className="pulse-ring" />
                                    <div className="pulse-ring" />
                                </div>
                            )}
                        </>
                    )}
                </div>
            </button>

            <div className="recorder-status">
                {isRecording && <span className="status-text recording">Recording...</span>}
                {isProcessing && <span className="status-text processing">Processing...</span>}
                {!isRecording && !isProcessing && (
                    <span className="status-text idle">Press and hold to speak</span>
                )}
            </div>

            {error && (
                <div className="error-message fade-in">
                    <svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z" />
                    </svg>
                    {error}
                </div>
            )}
        </div>
    );
};
