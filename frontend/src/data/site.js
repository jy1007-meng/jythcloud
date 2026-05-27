export const members = [
  {id:'jy', name:'吉天宇', avatar:'吉', role:'数据科学 & AI 创业者', accent:'#059669',
   about:'吉天宇是JYTHCloud团队的技术核心，主导了团队AI产品方向的确立和技术架构的搭建。从大二开始自学AI，一年内掌握了从模型调用到应用开发的完整链路。',
   edu:'湖北工程学院 · 数据科学与大数据技术（本科）',
   skills:['Python','机器学习','大模型API','数据分析','PyTorch','Docker','Linux','Git'],
   exp:[{t:'JYTHCloud · AI 技术负责人', p:'2025 - 至今', d:'负责团队AI技术方向探索、大模型应用开发与智能体构建，搭建了团队网站和API服务。'},
        {t:'量化交易回测系统', p:'2025 个人项目', d:'使用 Python + Pandas 搭建了A股量化回测系统，支持多因子策略回测。'},
        {t:'AI 自学与实践', p:'2024 - 至今', d:'自学大模型API调用、LangChain框架、机器学习建模，完成多个AI应用原型项目。'}],
   contact:{gh:'https://github.com/ji-tianyu', email:'ji@jythcloud.cn'}},
  {id:'tan', name:'谭海涛', avatar:'谭', role:'项目管理 & 执行负责人', accent:'#f59e0b',
   about:'谭海涛是JYTHCloud团队的项目管理担当。他擅长将复杂任务拆解为可执行的步骤，确保每个项目都能按时高质量交付。',
   edu:'湖北工程学院 · 数据科学与大数据技术（本科）',
   skills:['项目管理','敏捷开发','Python','数据分析','团队协作','文档规范'],
   exp:[{t:'JYTHCloud · 项目执行负责人', p:'2025 - 至今', d:'统筹团队项目进度管理，制定开发计划与里程碑，确保各个项目按时交付。'},
        {t:'团队网站建设项目', p:'2025', d:'协助搭建JYTHCloud团队官网及三个子站，负责内容规划、进度跟踪与上线验收。'},
        {t:'数据科学课程项目', p:'2024 - 至今', d:'参与多个数据分析课程项目，完成电商数据清洗、用户行为分析等实践任务。'}],
   contact:{gh:'https://github.com/tan-haitao', email:'tan@jythcloud.cn'}},
  {id:'hu', name:'胡子雄', avatar:'胡', role:'商务拓展 & 客户成功', accent:'#db2777',
   about:'胡子雄是JYTHCloud团队的商务与运营担当。他负责团队对外沟通、品牌建设和商业合作探索，致力于将团队的技术能力转化为实际价值。',
   edu:'湖北工程学院 · 数据科学与大数据技术（本科）',
   skills:['商务拓展','客户沟通','Python入门','品牌运营','数据可视化','团队管理'],
   exp:[{t:'JYTHCloud · 商务与运营负责人', p:'2025 - 至今', d:'负责团队品牌建设、对外沟通与商业合作探索，维护团队网站与社交媒体。'},
        {t:'校内创业项目', p:'2024 - 2025', d:'参与校内创业竞赛，负责项目路演和商业计划书撰写，积累了创业实战经验。'},
        {t:'数据可视化实践', p:'2025', d:'学习数据可视化工具，参与团队数据大屏的设计与开发。'}],
   contact:{gh:'https://github.com/zixiong-hu', email:'hu@jythcloud.cn'}}
]

export const services = [
  {icon:'fa-comment-dots',title:'大模型应用',href:'/posts/llm-api-guide.html',desc:'学习与探索大模型API的调用与集成，尝试开发智能对话、知识问答等应用原型。',items:['大模型 API 调用与 Prompt 调试','本地知识库问答系统搭建','多轮对话应用开发实践']},
  {icon:'fa-robot',title:'AI 智能体 (Agent)',href:'/posts/agent-intro.html',desc:'研究智能体框架，尝试构建能自主调用工具的 AI Agent，探索自动化工作流的可能性。',items:['LangChain / LangGraph 框架实践','工具调用与 API 编排','自动化信息采集与整理']},
  {icon:'fa-chart-bar',title:'数据智能分析',href:'/posts/data-analysis.html',desc:'运用Python、Pandas等工具，对公开数据进行清洗、建模与可视化分析。',items:['Python 数据分析与可视化','机器学习基础建模实践','数据大屏与报表开发']},
  {icon:'fa-server',title:'网站与云服务',href:'/posts/server-setup.html',desc:'从零搭建服务器架构，学习 Docker、Nginx、数据库部署与运维。',items:['Docker 容器化部署','Nginx 反向代理与 HTTPS','Flask / WordPress 后端开发']},
  {icon:'fa-camera',title:'计算机视觉入门',href:'/posts/cv-intro.html',desc:'通过课程项目学习图像分类、目标检测等基础视觉任务。',items:['OpenCV 图像处理基础','目标检测模型调用','OCR 文字识别实践']},
  {icon:'fa-graduation-cap',title:'技术学习与分享',href:'/posts/self-study-roadmap.html',desc:'通过博客记录学习历程，与更多同学交流AI学习路上的经验和踩坑记录。',items:['AI 学习路线与笔记分享','项目实战经验总结','大学生技术社区建设']}
]

export const about = [
  {icon:'fa-lightbulb',title:'我们的初心',href:'/posts/about-origin.html',desc:'我们相信 AI 是未来最重要的技术方向之一。作为数据科学专业的学生，我们希望把课堂上学到的知识真正用起来。'},
  {icon:'fa-flask',title:'我们在做什么',href:'/posts/about-action.html',desc:'课余时间自学大模型、智能体、数据分析等前沿技术，动手搭建服务器、开发小项目、写技术博客。'},
  {icon:'fa-handshake',title:'我们能做什么',href:'/posts/about-can-do.html',desc:'如果你有数据相关的需求、想找人一起做项目、或者想交流 AI 学习经验，欢迎联系我们一起探讨。'},
  {icon:'fa-globe',title:'我们的社区',href:'/posts/about-community.html',desc:'我们在团队博客中持续更新学习笔记和项目复盘，希望能帮助到更多同样在自学路上的同学。'}
]

export const articles = [
  {title:'JYTHCloud 团队正式成立', date:'2026-05-26', cat:'团队动态', href:'/posts/jythcloud-launch.html', desc:'我们很兴奋地宣布，JYTHCloud 团队正式成立了！'},
  {title:'JYTHCloud 技术栈揭秘', date:'2026-05-26', cat:'技术', href:'/posts/jythcloud-tech-stack.html', desc:'很多朋友问我们团队用什么技术栈。今天写一篇文章，详细介绍一下 JYTHCloud 背后的技术选型。'},
  {title:'大二自学 AI 一年复盘', date:'2026-05-26', cat:'学习笔记', href:'/posts/self-taught-ai-journey.html', desc:'大二那年我开始自学 AI。回头看一年多，最大的感悟是：光看教程没用，动手才是硬道理。'},
  {title:'AI 创业的几点思考', date:'2026-05-26', cat:'创业思考', href:'/posts/ai-startup-thoughts-2025.html', desc:'作为在校生做 AI 创业，我们总结出几条适合小团队的切入点。'},
  {title:'从零搭建量化交易回测系统', date:'2026-05-26', cat:'项目实战', href:'/posts/building-quant-backtest-system.html', desc:'量化交易一直是我感兴趣的方向。'},
  {title:'LLM API 接入指南', date:'2026-05-26', cat:'教程', href:'/posts/llm-api-guide.html', desc:'从零开始完成大模型 API 的注册、调试，并搭建你的第一个 AI 对话应用。'},
  {title:'AI Agent 入门', date:'2026-05-26', cat:'教程', href:'/posts/agent-intro.html', desc:'AI Agent 是当下最热门的方向之一。'}
]
