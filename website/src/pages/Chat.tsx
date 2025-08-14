/**
 * AI对话页面组件
 */

import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { ScrollArea } from '../components/ui/scroll-area';
import { Separator } from '../components/ui/separator';
import { Send, LogOut, Loader2, Bot, User, Wifi, WifiOff } from 'lucide-react';
import { chatWithDeepSeek, testDeepSeekConnection } from '../services/api';
import { ChatMessage } from '../types';

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentAIResponse, setCurrentAIResponse] = useState('');
  const [deepSeekConnected, setDeepSeekConnected] = useState<boolean | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();

  // 检查登录状态
  useEffect(() => {
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    if (!isLoggedIn) {
      navigate('/');
      return;
    }

    // 测试DeepSeek API连接
    const checkDeepSeekConnection = async () => {
      try {
        const isConnected = await testDeepSeekConnection();
        setDeepSeekConnected(isConnected);
        
        // 添加欢迎消息
        const welcomeMessage: ChatMessage = {
          id: Date.now().toString(),
          content: isConnected 
            ? '您好！我是AI助手，有什么可以帮助您的吗？'
            : '您好！我是AI助手，但检测到DeepSeek API连接异常，请检查网络连接或API密钥配置。',
          role: 'assistant',
          timestamp: new Date(),
        };
        setMessages([welcomeMessage]);
      } catch (error) {
        console.error('DeepSeek连接测试失败:', error);
        setDeepSeekConnected(false);
        
        const errorMessage: ChatMessage = {
          id: Date.now().toString(),
          content: '您好！检测到DeepSeek API连接失败，请检查网络连接或API密钥配置。',
          role: 'assistant',
          timestamp: new Date(),
        };
        setMessages([errorMessage]);
      }
    };

    checkDeepSeekConnection();
  }, [navigate]);

  // 滚动到底部
  useEffect(() => {
    scrollToBottom();
  }, [messages, currentAIResponse]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      content: inputValue.trim(),
      role: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setCurrentAIResponse('');

    try {
      console.log('开始AI对话，当前消息数量:', messages.length);
      
      // 准备发送给AI的消息历史
      const apiMessages = messages.map(msg => ({
        role: msg.role,
        content: msg.content,
      }));
      
      // 添加当前用户消息
      apiMessages.push({
        role: 'user',
        content: userMessage.content,
      });

      console.log('准备发送的消息:', apiMessages);

      // 调用DeepSeek API
      let fullResponse = '';
      await chatWithDeepSeek(apiMessages, (chunk) => {
        console.log('收到AI回复片段:', chunk);
        fullResponse += chunk;
        setCurrentAIResponse(fullResponse);
      });

      console.log('AI对话完成，完整回复:', fullResponse);

      // 完成AI回复后添加到消息列表
      if (fullResponse) {
        const aiMessage: ChatMessage = {
          id: Date.now().toString(),
          content: fullResponse,
          role: 'assistant',
          timestamp: new Date(),
        };
        setMessages(prev => [...prev, aiMessage]);
      }
    } catch (error) {
      console.error('AI对话错误详情:', error);
      const errorMessage: ChatMessage = {
        id: Date.now().toString(),
        content: `抱歉，发生了错误，请稍后重试。\n\n错误详情: ${error instanceof Error ? error.message : '未知错误'}`,
        role: 'assistant',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      // 延迟清空当前回复，确保UI有时间显示完整内容
      setTimeout(() => {
        setCurrentAIResponse('');
      }, 100);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('userInfo');
    navigate('/');
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('zh-CN', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* 顶部导航栏 */}
      <Card className="border-b rounded-none">
        <CardHeader className="py-4">
          <div className="flex items-center justify-between">
            <CardTitle className="text-xl font-semibold flex items-center">
              <Bot className="mr-2 h-5 w-5" />
              AI对话平台
            </CardTitle>
            <Button 
              variant="outline" 
              onClick={handleLogout}
              className="bg-transparent"
            >
              <LogOut className="mr-2 h-4 w-4" />
              退出登录
            </Button>
          </div>
        </CardHeader>
      </Card>

      {/* 对话区域 */}
      <div className="flex-1 p-4 max-w-4xl mx-auto w-full">
        <Card className="h-[calc(100vh-200px)]">
          <CardContent className="p-0 h-full flex flex-col">
            <ScrollArea className="flex-1 p-4">
              <div className="space-y-4">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[80%] rounded-lg px-4 py-2 ${
                        message.role === 'user'
                          ? 'bg-blue-500 text-white'
                          : 'bg-gray-100 text-gray-800'
                      }`}
                    >
                      <div className="flex items-center mb-1">
                        {message.role === 'user' ? (
                          <User className="h-4 w-4 mr-1" />
                        ) : (
                          <Bot className="h-4 w-4 mr-1" />
                        )}
                        <span className="text-xs opacity-75">
                          {message.role === 'user' ? '我' : 'AI助手'}
                        </span>
                        <span className="text-xs opacity-75 ml-2">
                          {formatTime(message.timestamp)}
                        </span>
                      </div>
                      <div className="text-sm whitespace-pre-wrap">
                        {message.content}
                      </div>
                    </div>
                  </div>
                ))}

                {/* 当前AI回复（流式显示） */}
                {currentAIResponse && (
                  <div className="flex justify-start">
                    <div className="max-w-[80%] rounded-lg px-4 py-2 bg-gray-100 text-gray-800">
                      <div className="flex items-center mb-1">
                        <Bot className="h-4 w-4 mr-1" />
                        <span className="text-xs opacity-75">AI助手</span>
                        <span className="text-xs opacity-75 ml-2">
                          {new Date().toLocaleTimeString('zh-CN', { 
                            hour: '2-digit', 
                            minute: '2-digit' 
                          })}
                        </span>
                      </div>
                      <div className="text-sm whitespace-pre-wrap">
                        {currentAIResponse}
                        {isLoading && <span className="inline-block w-2 h-4 bg-gray-400 ml-1 animate-pulse"></span>}
                      </div>
                    </div>
                  </div>
                )}

                <div ref={messagesEndRef} />
              </div>
            </ScrollArea>

            <Separator />

            {/* 输入区域 */}
            <div className="p-4">
              <div className="flex gap-2">
                <Input
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="输入您的问题..."
                  disabled={isLoading}
                  className="flex-1"
                />
                <Button 
                  onClick={handleSend} 
                  disabled={!inputValue.trim() || isLoading}
                >
                  {isLoading ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <Send className="h-4 w-4" />
                  )}
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
