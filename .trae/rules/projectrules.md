step1. 当用户提交URL和提示时，通过工具（可提示用户扩展工具），分析URL里的视频内容，改写成人物刻画、场景刻画、事件描述、动作描述、镜头轨迹、场景描述等，保存在scripts/1video_description.txt文件中
step2. 根据原视频和人物刻画生成主要人物的形象图片，保存在charectorImages文件夹下，每个图片命名为charectorImage_{name}.jpg，并且为每个人物更新类，保存在charectors文件夹下，每个文件命名为{name}.py
step3. 根据原视频和场景刻画生成主要场景的形象图片，保存在backgroundImages文件夹下，每个图片命名为background_{name}.jpg，并且为每个场景更新类，保存在backgrounds文件夹下，每个文件命名为{name}.py
step4. 结合用户提示，生成新的脚本scripts/script_{index}.txt，每个script.txt文件包含一个3～5秒事件描述，保存在scripts/script_{index}.txt文件中
step5. 根据scripts/script_{index}.txt事件脚本和charectorImagess、backgrounds文件夹下的人物刻画，生成每个事件描述的首尾帧，保存在frames文件夹下，每个帧命名为frame_{index}.jpg
step6. 调用视频生成工具，根据scripts和frames文件夹下的事件脚本和帧，生成新的片段放到footages文件夹下, 每个片段命名为footage_{index}.mp4
step7. 把footage目录下的脚本视频拼接，生成新的视频，命名为output.mp4，放到主目录下