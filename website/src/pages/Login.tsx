/**
 * 登录页面组件
 */

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Label } from '../components/ui/label';
import { Alert, AlertDescription } from '../components/ui/alert';
import { Loader2, Wifi, WifiOff } from 'lucide-react';
import { login, testApiConnection, API_BASE_URL } from '../services/api';
import { LoginRequest } from '../types';

export default function LoginPage() {
  const [formData, setFormData] = useState<LoginRequest>({
    username: '',
    password: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [apiConnected, setApiConnected] = useState<boolean | null>(null);
  const navigate = useNavigate();

  // 测试API连接
  useEffect(() => {
    const checkConnection = async () => {
      try {
        const isConnected = await testApiConnection();
        setApiConnected(isConnected);
        if (!isConnected) {
          setError('无法连接到API服务器，请检查网络连接或联系管理员');
        }
      } catch (error) {
        console.error('连接测试失败:', error);
        setApiConnected(false);
        setError('API服务器连接测试失败');
      }
    };

    checkConnection();
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    setError('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.username || !formData.password) {
      setError('请输入学工号和密码');
      return;
    }

    setLoading(true);
    setError('');

    try {
      console.log('正在发送登录请求:', formData);
      const response = await login(formData);
      console.log('登录响应:', response);
      
      if (response.success) {
        // 存储登录状态
        localStorage.setItem('isLoggedIn', 'true');
        localStorage.setItem('userInfo', JSON.stringify({
          user_type: response.user_type,
          user_id: response.user_id,
          username: formData.username,
        }));
        
        console.log('登录成功，跳转到聊天页面');
        // 跳转到聊天页面
        navigate('/chat');
      } else {
        console.log('登录失败:', response.message);
        setError(response.message || '登录失败');
      }
    } catch (error) {
      console.error('登录错误详情:', error);
      setError(`网络错误，请稍后重试。错误信息: ${error instanceof Error ? error.message : '未知错误'}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <div className="flex items-center justify-center mb-2">
            {apiConnected === null ? (
              <Loader2 className="h-5 w-5 animate-spin text-gray-500" />
            ) : apiConnected ? (
              <Wifi className="h-5 w-5 text-green-500" />
            ) : (
              <WifiOff className="h-5 w-5 text-red-500" />
            )}
            <span className="ml-2 text-sm text-gray-600">
              {apiConnected === null ? '正在检查连接...' : 
               apiConnected ? 'API服务器已连接' : 'API服务器连接失败'}
            </span>
          </div>
          <CardTitle className="text-2xl font-bold text-gray-800">AI对话平台</CardTitle>
          <CardDescription className="text-gray-600">
            请输入您的学工号和密码进行登录
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="username">学工号</Label>
              <Input
                id="username"
                name="username"
                type="text"
                placeholder="请输入学工号"
                value={formData.username}
                onChange={handleInputChange}
                disabled={loading || !apiConnected}
                className="w-full"
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="password">密码</Label>
              <Input
                id="password"
                name="password"
                type="password"
                placeholder="请输入密码"
                value={formData.password}
                onChange={handleInputChange}
                disabled={loading || !apiConnected}
                className="w-full"
              />
            </div>

            {error && (
              <Alert variant="destructive">
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            <Button 
              type="submit" 
              className="w-full" 
              disabled={loading || !apiConnected}
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  登录中...
                </>
              ) : (
                '登录'
              )}
            </Button>
          </form>
          
          {/* 调试按钮 - 跳过登录 */}
          <div className="mt-6 pt-4 border-t border-gray-200">
            <Button 
              variant="outline" 
              className="w-full bg-transparent"
              onClick={() => {
                // 设置临时登录状态
                localStorage.setItem('isLoggedIn', 'true');
                localStorage.setItem('userInfo', JSON.stringify({
                  user_type: 'debug_user',
                  user_id: 999999,
                  username: 'debug_user',
                }));
                navigate('/chat');
              }}
            >
              <span className="text-orange-600">🔧 调试模式 - 跳过登录</span>
            </Button>
            <p className="text-xs text-gray-500 mt-2 text-center">
              此按钮仅用于调试目的，临时跳过登录验证
            </p>
          </div>
          
          {apiConnected === false && (
            <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-md">
              <p className="text-sm text-yellow-800">
                <strong>调试信息：</strong><br />
                • API服务器地址: {API_BASE_URL}<br />
                • 请检查网络连接<br />
                • 确认API服务器正在运行<br />
                • 检查浏览器控制台获取详细错误信息
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
