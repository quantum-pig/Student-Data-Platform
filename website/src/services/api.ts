/**
 * API服务文件
 */

import { LoginRequest, LoginResponse, DeepSeekRequest, DeepSeekStreamChunk } from '../types';

/**
 * API基础配置
 */
export const API_BASE_URL = 'http://119.45.167.11:8000'; // API服务器地址

/**
 * 测试API服务器连接
 */
export const testApiConnection = async (): Promise<boolean> => {
  try {
    console.log('=== API服务器连接测试 ===');
    console.log('1. 测试URL:', `${API_BASE_URL}/health`);
    console.log('2. 测试方法: GET');
    console.log('3. 测试时间:', new Date().toISOString());
    
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    console.log('4. 健康检查响应状态:', response.status);
    console.log('5. 健康检查响应状态文本:', response.statusText);
    console.log('6. 健康检查响应头:');
    response.headers.forEach((value, key) => {
      console.log(`   ${key}: ${value}`);
    });
    
    if (response.ok) {
      try {
        const responseText = await response.text();
        console.log('7. 健康检查响应体:', responseText);
        console.log('=== API服务器连接测试成功 ===');
        return true;
      } catch (textError) {
        console.error('8. 读取健康检查响应体失败:', textError);
        console.log('=== API服务器连接测试部分成功 ===');
        return true; // 状态码正常，认为连接成功
      }
    } else {
      let errorText = '';
      try {
        errorText = await response.text();
        console.log('9. 健康检查错误响应体:', errorText);
      } catch (textError) {
        console.error('10. 读取健康检查错误响应体失败:', textError);
      }
      console.log('=== API服务器连接测试失败 ===');
      return false;
    }
  } catch (error) {
    console.error('=== API服务器连接测试异常 ===');
    console.error('异常类型:', error instanceof Error ? error.constructor.name : typeof error);
    console.error('异常消息:', error instanceof Error ? error.message : String(error));
    console.error('异常时间:', new Date().toISOString());
    console.error('=== API服务器连接测试异常结束 ===');
    return false;
  }
};
const DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions';
const DEEPSEEK_API_KEY = 'sk-b795ed6d14a34e85bc77b5bcd88cf253';

/**
 * 测试DeepSeek API连接
 */
export const testDeepSeekConnection = async (): Promise<boolean> => {
  try {
    console.log('测试DeepSeek API连接...');
    
    const testRequest: DeepSeekRequest = {
      model: 'deepseek-chat',
      messages: [{ role: 'user', content: 'Hello' }],
      stream: false,
      temperature: 0.7,
    };

    const response = await fetch(DEEPSEEK_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${DEEPSEEK_API_KEY}`,
      },
      body: JSON.stringify(testRequest),
    });

    const result = response.ok;
    console.log('DeepSeek API连接测试结果:', result, '状态码:', response.status);
    
    if (!result) {
      const errorText = await response.text();
      console.error('DeepSeek API连接测试失败:', errorText);
    }
    
    return result;
  } catch (error) {
    console.error('DeepSeek API连接测试异常:', error);
    return false;
  }
};

/**
 * 登录API调用
 * @param data 登录请求数据
 * @returns 登录响应
 */
export const login = async (data: LoginRequest): Promise<LoginResponse> => {
  try {
    // 详细的请求信息
    const requestUrl = `${API_BASE_URL}/login`;
    const requestBody = JSON.stringify(data);
    
    console.log('=== 登录API调试信息 ===');
    console.log('1. 请求URL:', requestUrl);
    console.log('2. 请求方法: POST');
    console.log('3. 请求头:', {
      'Content-Type': 'application/json',
    });
    console.log('4. 请求体:', requestBody);
    console.log('5. 请求时间:', new Date().toISOString());
    
    // 发送请求
    const response = await fetch(requestUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: requestBody,
    });

    // 详细的响应信息
    console.log('6. 响应状态:', response.status);
    console.log('7. 响应状态文本:', response.statusText);
    console.log('8. 响应头信息:');
    response.headers.forEach((value, key) => {
      console.log(`   ${key}: ${value}`);
    });

    // 检查响应状态
    if (!response.ok) {
      let errorText = '';
      try {
        errorText = await response.text();
        console.log('9. 错误响应体:', errorText);
      } catch (textError) {
        console.error('10. 读取错误响应体失败:', textError);
        errorText = '无法读取错误响应体';
      }
      
      // 尝试解析JSON错误
      try {
        const errorJson = JSON.parse(errorText);
        console.log('11. 解析后的错误JSON:', errorJson);
      } catch (jsonError) {
        console.log('12. 错误响应不是有效的JSON格式');
      }
      
      throw new Error(`HTTP ${response.status}: ${errorText || '登录请求失败'}`);
    }

    // 成功响应处理
    let responseData: LoginResponse;
    try {
      responseData = await response.json();
      console.log('13. 成功响应数据:', responseData);
    } catch (jsonError) {
      console.error('14. 解析成功响应JSON失败:', jsonError);
      const responseText = await response.text();
      console.log('15. 原始响应文本:', responseText);
      throw new Error(`响应JSON解析失败: ${responseText}`);
    }

    // 验证响应数据结构
    console.log('16. 响应数据验证:');
    console.log('   - success:', typeof responseData.success, responseData.success);
    console.log('   - message:', typeof responseData.message, responseData.message);
    console.log('   - user_type:', typeof responseData.user_type, responseData.user_type);
    console.log('   - user_id:', typeof responseData.user_id, responseData.user_id);

    if (typeof responseData.success !== 'boolean') {
      console.error('17. 响应数据格式错误: success字段不是布尔值');
      throw new Error('响应数据格式错误: success字段不是布尔值');
    }

    console.log('=== 登录API调用完成 ===');
    return responseData;
  } catch (error) {
    console.error('=== 登录API调用异常 ===');
    console.error('异常类型:', error instanceof Error ? error.constructor.name : typeof error);
    console.error('异常消息:', error instanceof Error ? error.message : String(error));
    console.error('异常堆栈:', error instanceof Error ? error.stack : '无堆栈信息');
    console.error('异常时间:', new Date().toISOString());
    console.error('=== 登录API异常结束 ===');
    throw error;
  }
};

/**
 * 调用DeepSeek API进行对话
 * @param messages 对话消息列表
 * @param onStream 流式响应回调
 */
export const chatWithDeepSeek = async (
  messages: Array<{ role: string; content: string }>,
  onStream: (chunk: string) => void
): Promise<void> => {
  try {
    console.log('开始调用DeepSeek API...');
    
    // 修复类型不兼容问题，将messages的role字段限制为"user" | "assistant" | "system"
    const request: DeepSeekRequest = {
      model: 'deepseek-chat',
      messages: messages.map(msg => ({
        role: msg.role as "user" | "assistant" | "system",
        content: msg.content
      })),
      stream: true,
      temperature: 0.7,
    };

    console.log('DeepSeek API请求:', {
      url: DEEPSEEK_API_URL,
      model: request.model,
      messageCount: request.messages.length,
      hasApiKey: !!DEEPSEEK_API_KEY
    });

    const response = await fetch(DEEPSEEK_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${DEEPSEEK_API_KEY}`,
      },
      body: JSON.stringify(request),
    });

    console.log('DeepSeek API响应状态:', response.status);
    console.log('DeepSeek API响应头:', Object.fromEntries(response.headers.entries()));

    if (!response.ok) {
      const errorText = await response.text();
      console.error('DeepSeek API错误响应:', errorText);
      throw new Error(`DeepSeek API请求失败: HTTP ${response.status} - ${errorText}`);
    }

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();

    if (!reader) {
      throw new Error('无法获取响应流');
    }

    console.log('开始读取流数据...');
    let totalChunks = 0;

    while (true) {
      const { done, value } = await reader.read();
      
      if (done) {
        console.log('流数据读取完成，总共处理了', totalChunks, '个数据块');
        break;
      }

      const chunk = decoder.decode(value, { stream: true });
      const lines = chunk.split('\n');
      totalChunks++;

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6);
          
          if (data === '[DONE]') {
            console.log('收到流结束标记');
            return;
          }

          try {
            const parsed: DeepSeekStreamChunk = JSON.parse(data);
            const content = parsed.choices[0]?.delta?.content || '';
            
            if (content) {
              onStream(content);
            }
          } catch (e) {
            console.error('解析流数据错误:', e, '原始数据:', data);
          }
        }
      }
    }
  } catch (error) {
    console.error('DeepSeek API调用错误:', error);
    throw error;
  }
};
