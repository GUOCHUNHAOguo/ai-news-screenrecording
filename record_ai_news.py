#!/usr/bin/env python3
"""
AI新闻搜索录屏脚本
自动打开浏览器，搜索AI新闻，录屏并上传到GitHub
"""

import asyncio
from playwright.async_api import async_playwright
import os
import subprocess
from datetime import datetime

async def main():
    video_path = "/Users/veck.liu/ai-news-screenrecording/screenrecording.mp4"
    
    async with async_playwright() as p:
        # 启动浏览器，开启录屏
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            record_video_dir="/Users/veck.liu/ai-news-screenrecording/",
            record_video_size={'width': 1920, 'height': 1080}
        )
        
        page = await context.new_page()
        
        # 打开Google搜索AI新闻
        print("正在打开浏览器搜索AI新闻...")
        await page.goto("https://www.google.com/search?q=AI+news+latest")
        
        # 等待页面加载
        await page.wait_for_timeout(3000)
        
        # 滚动页面展示更多内容
        print("正在滚动页面...")
        await page.evaluate("window.scrollBy(0, 500)")
        await page.wait_for_timeout(2000)
        
        # 截图留念
        print("截图保存...")
        await page.screenshot(path="/Users/veck.liu/ai-news-screenrecording/screenshot.png")
        
        # 再滚动一次
        await page.evaluate("window.scrollBy(0, 500)")
        await page.wait_for_timeout(2000)
        
        # 关闭浏览器并保存视频
        print("关闭浏览器，保存视频...")
        await browser.close()
        
        # 重命名视频文件
        video_files = [f for f in os.listdir("/Users/veck.liu/ai-news-screenrecording/") if f.endswith('.webm')]
        if video_files:
            os.rename(
                f"/Users/veck.liu/ai-news-screenrecording/{video_files[0]}",
                video_path
            )
            print(f"视频已保存到: {video_path}")
        else:
            print("警告: 没有找到视频文件")
        
        # 创建README
        readme_content = f"""# AI新闻搜索录屏演示

## 录制时间
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 录制内容
自动打开浏览器，搜索并浏览最新的AI新闻。

## 文件说明
- `screenrecoding.mp4` - 录屏视频
- `screenshot.png` - 截图
"""
        
        with open("/Users/veck.liu/ai-news-screenrecording/README.md", "w") as f:
            f.write(readme_content)
        
        print("✅ 录屏完成！请手动推送代码到GitHub。")

if __name__ == "__main__":
    asyncio.run(main())
