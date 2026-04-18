import React, { useState, useRef, useEffect } from 'react';
import { Send, Mic, Volume2, Copy, Loader, Trash2, Plus, MessageCircle, Paperclip, X } from 'lucide-react';
import { useLanguage } from '@/context/LanguageContext';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  language?: string;
  feature?: string;
  attachments?: Array<{
    type: 'image' | 'pdf';
    name: string;
    data?: string;
  }>;
}

interface Conversation {
  id: string;
  title: string;
  timestamp: Date;
}

const UnifiedChatbot: React.FC = () => {
  const { t } = useLanguage();
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [attachedFiles, setAttachedFiles] = useState<Array<{ type: 'image' | 'pdf'; name: string; data: string }>>([]);
  const recognitionRef = useRef<any>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Initialize speech recognition
  useEffect(() => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (SpeechRecognition) {
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;

      recognitionRef.current.onstart = () => {
        setIsListening(true);
      };

      recognitionRef.current.onend = () => {
        setIsListening(false);
      };

      recognitionRef.current.onresult = (event: any) => {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          transcript += event.results[i][0].transcript;
        }
        setInputText(transcript);
      };

      recognitionRef.current.onerror = (event: any) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
      };
    }
  }, []);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const startListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.start();
    }
  };

  const stopListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
  };

  const handleSendMessage = async () => {
    if (!inputText.trim() && attachedFiles.length === 0) return;

    // Add user message
    const userMessage: Message = {
      id: `u-${Date.now()}`,
      role: 'user',
      content: inputText || (attachedFiles.length > 0 ? `Sent ${attachedFiles.length} file(s)` : ''),
      timestamp: new Date(),
      attachments: attachedFiles,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputText('');
    setAttachedFiles([]);
    setIsLoading(true);

    try {
      // Prepare conversation history for context
      const history = messages.map((msg) => ({
        role: msg.role,
        content: msg.content,
      }));

      const response = await fetch('http://localhost:5000/api/chatbot/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: inputText || `Analyzing ${attachedFiles.length} file(s)`,
          history: history,
          attachments: attachedFiles,
        }),
      });

      const data = await response.json();

      if (data.success) {
        const assistantMessage: Message = {
          id: `a-${Date.now()}`,
          role: 'assistant',
          content: data.response,
          timestamp: new Date(),
          language: data.language,
          feature: data.feature,
        };

        setMessages((prev) => [...prev, assistantMessage]);

        // Auto-speak response
        speakText(data.response);
      } else {
        const errorMessage: Message = {
          id: `e-${Date.now()}`,
          role: 'assistant',
          content: data.error || 'Error processing message',
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, errorMessage]);
      }
    } catch (err) {
      console.error(err);
      const errorMessage: Message = {
        id: `e-${Date.now()}`,
        role: 'assistant',
        content: 'Error connecting to server',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const detectLanguage = (text: string): string => {
    // Check if text contains Devanagari script (Hindi)
    const hindiPattern = /[\u0900-\u097F]/;
    return hindiPattern.test(text) ? 'hi-IN' : 'en-IN';
  };

  const speakText = (text: string) => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      const language = detectLanguage(text);
      utterance.lang = language;
      utterance.rate = 0.9;
      utterance.pitch = 1;
      utterance.volume = 1;
      window.speechSynthesis.speak(utterance);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const clearChat = () => {
    if (window.confirm('Clear all messages?')) {
      setMessages([]);
    }
  };

  const startNewConversation = () => {
    const newId = `conv-${Date.now()}`;
    const newConv: Conversation = {
      id: newId,
      title: 'New Conversation',
      timestamp: new Date(),
    };
    setConversations([newConv, ...conversations]);
    setCurrentConversationId(newId);
    setMessages([]);
  };

  const loadConversation = (convId: string) => {
    setCurrentConversationId(convId);
    // In a real app, load messages from storage
    setMessages([]);
  };

  const handleFileSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (!files) return;

    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const isImage = file.type.startsWith('image/');
      const isPdf = file.type === 'application/pdf';

      if (!isImage && !isPdf) {
        alert('Please upload only images or PDF files');
        continue;
      }

      const reader = new FileReader();
      reader.onload = (e) => {
        const data = e.target?.result as string;
        setAttachedFiles((prev) => [
          ...prev,
          {
            type: isImage ? 'image' : 'pdf',
            name: file.name,
            data: data,
          },
        ]);
      };
      reader.readAsDataURL(file);
    }

    // Reset input
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const removeAttachment = (index: number) => {
    setAttachedFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const getFeatureIcon = (feature?: string) => {
    switch (feature) {
      case 'crop_recommendation':
        return '🌾';
      case 'fertilizer':
        return '🧪';
      case 'disease':
        return '🔍';
      case 'weather':
        return '🌤️';
      case 'reminders':
        return '📅';
      default:
        return '💬';
    }
  };

  return (
    <div 
      className="min-h-screen flex bg-gradient-to-br from-eco-green-dark via-eco-green to-eco-green-light"
    >
      {/* Left Sidebar */}
      <div className={`${sidebarOpen ? 'w-64' : 'w-0'} transition-all duration-300 bg-eco-green-dark border-r border-eco-green flex flex-col overflow-hidden`}>
        {/* New Chat Button */}
        <div className="p-4 border-b border-eco-green">
          <button
            onClick={startNewConversation}
            className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-gradient-to-r from-eco-yellow to-eco-yellow hover:brightness-110 text-eco-green-dark rounded-lg transition font-semibold"
          >
            <Plus className="w-5 h-5" />
            {t('chatbot.newChat')}
          </button>
        </div>

        {/* Conversations List */}
        <div className="flex-1 overflow-y-auto p-4 space-y-2">
          {conversations.length === 0 ? (
            <p className="text-eco-cream text-sm text-center py-8">{t('chatbot.noConversations')}</p>
          ) : (
            conversations.map((conv) => (
              <button
                key={conv.id}
                onClick={() => loadConversation(conv.id)}
                className={`w-full text-left px-3 py-2 rounded-lg transition flex items-center gap-2 ${
                  currentConversationId === conv.id
                    ? 'bg-eco-yellow text-eco-green-dark'
                    : 'text-primary-foreground hover:bg-eco-green'
                }`}
              >
                <MessageCircle className="w-4 h-4 flex-shrink-0" />
                <span className="truncate text-sm">{conv.title}</span>
              </button>
            ))
          )}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-gradient-to-r from-eco-green to-eco-teal text-white p-4 shadow-lg flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 hover:bg-white/20 rounded-lg transition"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
            <div>
              <h1 className="text-2xl font-bold">{t('chatbot.title')}</h1>
              <p className="text-sm opacity-90">{t('chatbot.subtitle')}</p>
            </div>
          </div>
          <button
            onClick={clearChat}
            className="px-4 py-2 bg-white/20 hover:bg-white/30 rounded-lg transition flex items-center gap-2"
          >
            <Trash2 className="w-4 h-4" /> {t('chatbot.clear')}
          </button>
        </div>

        {/* Chat Messages Area */}
        <div className="flex-1 overflow-y-auto p-6 flex flex-col">
          {messages.length === 0 ? (
            // Welcome Screen
            <div className="flex-1 flex flex-col items-center justify-center">
              <div className="text-center max-w-2xl">
                <h2 className="text-6xl font-bold text-white mb-2">🌾</h2>
                <h3 className="text-4xl font-bold text-white mb-2">KisanSathi</h3>
                <p className="text-xl text-eco-cream mb-12">Your AI Farming Assistant</p>

                {/* Quick Suggestions Grid */}
                <div className="grid grid-cols-2 gap-4 max-w-xl">
                  {[
                    {
                      icon: '🌾',
                      title: t('chatbot.cropSelection'),
                      desc: t('chatbot.cropSelectionDesc'),
                    },
                    {
                      icon: '🧪',
                      title: t('chatbot.fertilizer'),
                      desc: t('chatbot.fertilizerDesc'),
                    },
                    {
                      icon: '🔍',
                      title: t('chatbot.diseaseHelp'),
                      desc: t('chatbot.diseaseHelpDesc'),
                    },
                    {
                      icon: '🌤️',
                      title: t('chatbot.weatherAdvice'),
                      desc: t('chatbot.weatherAdviceDesc'),
                    },
                  ].map((item, i) => (
                    <button
                      key={i}
                      onClick={() => setInputText(item.desc)}
                      className="p-4 bg-eco-green/30 hover:bg-eco-green/50 backdrop-blur-md rounded-lg text-left transition border border-eco-yellow"
                    >
                      <div className="text-3xl mb-2">{item.icon}</div>
                      <div className="font-semibold text-white text-sm">{item.title}</div>
                      <div className="text-xs text-eco-cream">{item.desc}</div>
                    </button>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            // Chat Messages
            <div className="space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-2xl px-4 py-3 rounded-lg backdrop-blur-md ${
                      message.role === 'user'
                        ? 'bg-eco-yellow text-eco-green-dark rounded-br-none'
                        : 'bg-eco-green/30 text-primary-foreground rounded-bl-none border border-eco-yellow'
                    }`}
                  >
                    <div className="flex items-start gap-2">
                      {message.role === 'assistant' && (
                        <span className="text-xl flex-shrink-0">
                          {getFeatureIcon(message.feature)}
                        </span>
                      )}
                      <div className="flex-1">
                        <p className="text-sm leading-relaxed">{message.content}</p>
                        {message.attachments && message.attachments.length > 0 && (
                          <div className="mt-2 flex flex-wrap gap-2">
                            {message.attachments.map((att, idx) => (
                              <div key={idx} className="relative">
                                {att.type === 'image' && att.data ? (
                                  <img
                                    src={att.data}
                                    alt={att.name}
                                    className="max-w-xs max-h-48 rounded-lg border border-eco-yellow"
                                  />
                                ) : (
                                  <div className="px-3 py-2 bg-eco-green/50 rounded-lg border border-eco-yellow text-xs text-eco-cream">
                                    📄 {att.name}
                                  </div>
                                )}
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>

                    {message.role === 'assistant' && (
                      <div className="flex gap-2 mt-2 pt-2 border-t border-eco-green">
                        <button
                          onClick={() => speakText(message.content)}
                          className="text-xs opacity-70 hover:opacity-100 flex items-center gap-1 transition"
                        >
                          <Volume2 className="w-3 h-3" /> {t('chatbot.speak')}
                        </button>
                        <button
                          onClick={() => copyToClipboard(message.content)}
                          className="text-xs opacity-70 hover:opacity-100 flex items-center gap-1 transition"
                        >
                          <Copy className="w-3 h-3" /> {t('chatbot.copy')}
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-eco-green/30 text-primary-foreground px-4 py-3 rounded-lg rounded-bl-none border border-eco-yellow">
                    <Loader className="w-5 h-5 animate-spin" />
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="bg-eco-green-dark/50 backdrop-blur-md border-t border-eco-yellow p-4">
          <div className="max-w-4xl mx-auto">
            {/* Attached Files Preview */}
            {attachedFiles.length > 0 && (
              <div className="mb-3 flex flex-wrap gap-2">
                {attachedFiles.map((file, idx) => (
                  <div
                    key={idx}
                    className="flex items-center gap-2 px-3 py-2 bg-eco-green rounded-lg border border-eco-yellow"
                  >
                    {file.type === 'image' ? (
                      <img
                        src={file.data}
                        alt={file.name}
                        className="w-8 h-8 rounded object-cover"
                      />
                    ) : (
                      <div className="w-8 h-8 bg-red-600 rounded flex items-center justify-center text-white text-xs font-bold">
                        PDF
                      </div>
                    )}
                    <span className="text-sm text-slate-300 truncate max-w-xs">
                      {file.name}
                    </span>
                    <button
                      onClick={() => removeAttachment(idx)}
                      className="ml-auto text-slate-400 hover:text-slate-200"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                ))}
              </div>
            )}

            <div className="flex gap-3">
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileSelect}
                accept="image/*,.pdf"
                multiple
                className="hidden"
              />

              <button
                onClick={() => fileInputRef.current?.click()}
                className="px-4 py-3 bg-eco-green text-primary-foreground hover:bg-eco-green/80 rounded-full transition flex items-center gap-2 border border-eco-yellow"
                title={t('chatbot.uploadFile')}
              >
                <Plus className="w-5 h-5" />
              </button>

              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                placeholder={t('chatbot.placeholder')}
                className="flex-1 px-4 py-3 bg-eco-green text-primary-foreground rounded-full focus:ring-2 focus:ring-eco-yellow focus:border-transparent placeholder-primary-foreground/50 border border-eco-yellow"
              />

              <button
                onClick={isListening ? stopListening : startListening}
                className={`px-4 py-3 rounded-full font-semibold transition flex items-center gap-2 ${
                  isListening
                    ? 'bg-red-600 text-white hover:bg-red-700'
                    : 'bg-eco-yellow text-eco-green-dark hover:brightness-110'
                }`}
              >
                <Mic className="w-5 h-5" />
              </button>

              <button
                onClick={handleSendMessage}
                disabled={!inputText.trim() && attachedFiles.length === 0 || isLoading}
                className="px-4 py-3 bg-gradient-to-r from-eco-yellow to-eco-yellow text-eco-green-dark rounded-full hover:brightness-110 disabled:from-gray-600 disabled:to-gray-600 transition flex items-center gap-2"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UnifiedChatbot;
