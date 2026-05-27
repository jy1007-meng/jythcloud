<template>
  <div class="section-container">
    <!-- Hero 区域 -->
    <section class="hero-section">
      <div class="particles" ref="particles"></div>
      <h1 class="hero-title">从校园出发<br>探索 AI 的无限可能</h1>
      <p class="hero-subtitle">JYTHCloud · 湖北工程学院 · 大学生AI创业团队</p>
      <div class="hero-btns">
        <a href="#services" class="btn btn-primary" @click.prevent="scrollTo('services')"><i class="fas fa-arrow-down"></i> 了解我们</a>
        <a href="#posts" class="btn btn-outline" @click.prevent="scrollTo('posts')"><i class="fas fa-newspaper"></i> 阅读文章</a>
      </div>
    </section>

    <!-- 服务卡片 -->
    <section id="services" class="section">
      <h2 class="section-title">我们在探索的方向</h2>
      <p class="section-subtitle">作为在校生团队，我们在课堂学习之余不断尝试将 AI 技术落地</p>
      <div class="card-grid card-grid-3">
        <div v-for="s in services" :key="s.title" class="card service-card" @click="openLink(s.href)">
          <div class="card-icon"><i :class="'fas ' + s.icon"></i></div>
          <h3>{{ s.title }}</h3>
          <p>{{ s.desc }}</p>
          <ul class="features">
            <li v-for="item in s.items" :key="item"><i class="fas fa-check-circle"></i> {{ item }}</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- 关于我们 -->
    <section id="about" class="section">
      <h2 class="section-title">关于我们</h2>
      <p class="section-subtitle">三个在校生因为对 AI 的共同热爱走到了一起</p>
      <div class="card-grid card-grid-2">
        <div v-for="a in about" :key="a.title" class="card about-card" @click="openLink(a.href)">
          <div class="card-icon"><i :class="'fas ' + a.icon"></i></div>
          <h3>{{ a.title }}</h3>
          <p>{{ a.desc }}</p>
          <div class="card-readmore">阅读全文 <i class="fas fa-arrow-right"></i></div>
        </div>
      </div>
    </section>

    <!-- 文章列表 -->
    <section id="posts" class="section">
      <h2 class="section-title">最新文章</h2>
      <p class="section-subtitle">我们的技术分享与成长记录 — 点击卡片阅读全文</p>
      <div class="card-grid card-grid-3">
        <div v-for="a in articles" :key="a.title" class="card post-card" @click="openLink(a.href)">
          <div class="post-meta"><i class="far fa-calendar-alt"></i> {{ a.date }} <span class="post-cat">{{ a.cat }}</span></div>
          <h3>{{ a.title }}</h3>
          <p>{{ a.desc }}</p>
          <div class="card-readmore">阅读全文 <i class="fas fa-arrow-right"></i></div>
        </div>
      </div>
    </section>

    <!-- 底部 -->
    <footer>
      <p>© 2026 JYTHCloud · 湖北工程学院数据科学与大数据技术专业 · 大学生创业团队</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { services, about, articles } from '../data/site.js'

const particles = ref(null)

function scrollTo(id) {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}

function openLink(href) {
  if (href) window.open(href, '_blank')
}

onMounted(() => {
  // 粒子动画
  if (particles.value) {
    const c = particles.value
    for (let i = 0; i < 30; i++) {
      const p = document.createElement('div')
      p.className = 'particle'
      p.style.cssText = `left:${Math.random()*100}%;width:${1+Math.random()*2}px;height:${1+Math.random()*2}px;animation:${15+Math.random()*25}s linear ${Math.random()*20}s infinite`
      c.appendChild(p)
    }
  }

  // 导航菜单
  const toggle = document.getElementById('navToggle')
  const links = document.getElementById('navLinks')
  if (toggle && links) {
    toggle.onclick = () => links.classList.toggle('open')
    document.querySelectorAll('.nav-links a').forEach(a => {
      a.addEventListener('click', () => {
        links.classList.remove('open')
        const href = a.getAttribute('href')
        if (!href || href === '#' || href.startsWith('http')) return
        const id = href.slice(1).replace('-detail', '_detail')
        const el = document.getElementById(id)
        if (el) el.scrollIntoView({ behavior: 'smooth' })
      })
    })
  }
})
</script>

<style scoped>
.section-container {
  position: relative;
  z-index: 1;
}
.hero-section {
  position: relative;
  z-index: 1;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 120px 24px 80px;
}
.particles {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}
:deep(.particle) {
  position: absolute;
  border-radius: 50%;
  background: rgba(96, 165, 250, 0.2);
}
.hero-title {
  font-size: clamp(2.8rem, 8vw, 5.5rem);
  font-weight: 800;
  background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #f472b6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 16px;
  animation: fadeUp 0.8s ease-out;
  position: relative;
  z-index: 1;
}
.hero-subtitle {
  font-size: clamp(1rem, 2.5vw, 1.25rem);
  color: #999;
  margin-bottom: 40px;
  animation: fadeUp 0.8s ease-out 0.15s both;
  position: relative;
  z-index: 1;
}
.hero-btns {
  display: flex; gap: 16px; flex-wrap: wrap; justify-content: center;
  animation: fadeUp 0.8s ease-out 0.3s both;
  position: relative; z-index: 1;
}
.btn {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 14px 32px; border-radius: 50px;
  font-size: 1rem; font-weight: 600;
  text-decoration: none; transition: all 0.3s; cursor: pointer;
}
.btn-primary {
  background: linear-gradient(135deg, #60a5fa, #a78bfa);
  color: #fff; border: none;
}
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(96, 165, 250, 0.3);
}
.btn-outline {
  background: transparent; color: #e0e0e0;
  border: 1px solid rgba(255,255,255,0.07);
}
.btn-outline:hover {
  background: rgba(255,255,255,0.06);
  border-color: #60a5fa; color: #60a5fa;
}
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

.section {
  position: relative; z-index: 1;
  padding: 80px 24px; max-width: 1200px; margin: 0 auto;
}
.section-title {
  text-align: center;
  font-size: clamp(1.6rem, 4vw, 2.2rem);
  font-weight: 700; margin-bottom: 12px;
  background: linear-gradient(135deg, #60a5fa, #a78bfa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.section-subtitle {
  text-align: center; color: #999;
  font-size: 1rem; margin-bottom: 50px;
  max-width: 600px; margin-left: auto; margin-right: auto;
}

.card-grid {
  display: grid; gap: 20px;
}
.card-grid-3 { grid-template-columns: repeat(3, 1fr); }
.card-grid-2 { grid-template-columns: repeat(2, 1fr); }

.card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 14px;
  padding: 32px 24px;
  text-align: center;
  transition: all 0.3s;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, #60a5fa, #a78bfa);
  opacity: 0;
  transition: opacity 0.3s;
}
.card:hover::before { opacity: 1; }
.card:hover {
  background: rgba(255,255,255,0.06);
  border-color: #60a5fa;
  transform: translateY(-4px);
}
.card-icon {
  font-size: 2.2rem; margin-bottom: 14px;
  background: linear-gradient(135deg, #60a5fa, #a78bfa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.card h3 { font-size: 1.1rem; margin-bottom: 8px; color: #e0e0e0; }
.card p { font-size: 0.9rem; color: #999; line-height: 1.6; }
.card-readmore {
  margin-top: 14px;
  font-size: 0.82rem;
  color: #60a5fa;
  display: flex;
  align-items: center;
  gap: 6px;
  justify-content: center;
}
.card:hover .card-readmore { gap: 10px; }

.features {
  margin-top: 14px;
  text-align: left;
  font-size: 0.85rem;
  color: #999;
  list-style: none;
}
.features li {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 0;
}
.features li i { color: #22c55e; font-size: 0.75rem; }

.post-meta {
  font-size: 0.78rem;
  color: #666;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.post-cat {
  display: inline-block; padding: 2px 10px;
  border-radius: 50px; font-size: 0.72rem;
  background: rgba(96, 165, 250, 0.1);
  color: #60a5fa;
  border: 1px solid rgba(96, 165, 250, 0.15);
}
.post-card h3 { font-size: 1.05rem; margin-bottom: 10px; line-height: 1.4; }
.post-card p { font-size: 0.88rem; flex: 1; }

footer {
  position: relative; z-index: 1;
  text-align: center; padding: 40px 24px;
  border-top: 1px solid rgba(255,255,255,0.07);
  color: #666; font-size: 0.85rem;
}

/* 响应式 */
@media (max-width: 1024px) {
  .card-grid-3 { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 768px) {
  .card-grid, .card-grid-3, .card-grid-2 { grid-template-columns: 1fr; }
  .section { padding: 40px 16px; }
  .hero-section { padding: 90px 16px 50px; min-height: 90vh; }
  .hero-title { font-size: clamp(2rem, 9vw, 3rem); }
  .hero-btns { flex-direction: column; align-items: stretch; width: 100%; max-width: 320px; }
  .hero-btns .btn { justify-content: center; }
  .card { padding: 20px 16px; }
  .card:active { transform: scale(0.97); }
}
</style>
