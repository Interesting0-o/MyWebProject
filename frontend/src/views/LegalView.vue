<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useSeo } from '@/composables/useSeo'
import { site } from '@/config/site'
import { formatDate } from '@/utils/format'

const route = useRoute()

const documents = {
  privacy: {
    eyebrow: 'Privacy',
    title: '隐私政策',
    description: '了解本站会接触哪些信息，以及这些信息如何被使用。',
    updated: '2026-10-31',
    sections: [
      {
        heading: '我们收集的信息',
        paragraphs: [
          '本站是一个个人博客，不提供账号注册或支付功能，因此不会主动收集你的姓名、手机号、身份证号等个人身份信息。',
          '访问本站时，服务器或 CDN 可能记录常规访问日志，例如 IP 地址、浏览器类型、访问时间与请求路径。这些日志仅用于保障服务安全、排查故障和了解访问情况。',
        ],
      },
      {
        heading: '本地存储',
        paragraphs: [
          '为了记住你选择的白天或夜间模式，本站会使用浏览器 localStorage 保存一个 theme 值。该数据只保存在你的浏览器中，不会被上传到服务器。',
          '你可以通过浏览器设置随时清除这些本地数据，清除后站点会重新跟随系统外观。',
        ],
      },
      {
        heading: '评论',
        paragraphs: [
          '当你在文章页发表评论时，你提交的昵称、评论内容与提交时间会保存在本站服务器上，并公开展示在对应文章下方。请不要在评论中填写邮箱、电话、住址等敏感信息。',
          '目前发表评论不需要注册。站长可以手动隐藏不当内容；如果你希望删除自己发表的评论，可以通过下方联系方式与站长联系。',
        ],
      },
      {
        heading: '第三方服务',
        paragraphs: [
          '本站可能包含指向 GitHub、微博、X 等第三方网站的链接。离开本站后，这些网站会按照各自的隐私政策处理你的信息，本站无法控制其行为。',
        ],
      },
      {
        heading: '你的权利',
        paragraphs: [
          `如果你对隐私问题有疑问，或希望了解、删除访问日志与评论相关的信息，可以通过 ${site.author.email} 与站长联系。`,
        ],
      },
      {
        heading: '政策更新',
        paragraphs: ['本政策可能会随站点功能调整而更新，更新后会直接发布在本页面。'],
      },
    ],
  },
  disclaimer: {
    eyebrow: 'Disclaimer',
    title: '免责声明',
    description: '本站内容的适用范围与责任说明。',
    updated: '2026-10-31',
    sections: [
      {
        heading: '内容性质',
        paragraphs: [
          '本站所有文章均为站长的个人学习笔记与观点表达，不构成任何形式的技术保证、法律意见、投资建议或医疗建议。',
        ],
      },
      {
        heading: '内容准确性',
        paragraphs: [
          '站长会尽量确保内容准确，但无法保证所有信息始终最新或完全无误。技术发展迅速，请结合官方文档与你的实际环境进行判断。',
        ],
      },
      {
        heading: '外部链接',
        paragraphs: [
          '本站可能引用或链接到第三方网站与资源，其内容与可用性由相应网站负责，本站不对第三方内容承担责任。',
        ],
      },
      {
        heading: '版权与转载',
        paragraphs: [
          `除特别注明外，本站原创内容采用 ${site.license.name} 许可协议。商业使用或大规模转载前，请先与站长联系。`,
        ],
      },
      {
        heading: '责任限制',
        paragraphs: ['因使用或无法使用本站内容而产生的任何直接或间接损失，站长不承担法律责任。'],
      },
    ],
  },
}

const doc = computed(() => documents[route.name] ?? documents.privacy)

useSeo(() => ({
  title: doc.value.title,
  description: doc.value.description,
  keywords: [doc.value.title, site.name],
  path: route.path,
}))
</script>

<template>
  <div class="container container--narrow page legal">
    <header class="page-header">
      <p class="eyebrow">{{ doc.eyebrow }}</p>
      <h1 class="page-title">{{ doc.title }}</h1>
      <p class="page-description">{{ doc.description }}</p>
      <p class="legal-updated">最后更新：{{ formatDate(doc.updated) }}</p>
    </header>

    <section v-for="section in doc.sections" :key="section.heading" class="legal-section">
      <h2>{{ section.heading }}</h2>
      <p v-for="paragraph in section.paragraphs" :key="paragraph">{{ paragraph }}</p>
    </section>
  </div>
</template>

<style scoped>
.legal-updated {
  margin-top: 0.9rem;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.03em;
  color: var(--color-text-faint);
}

.legal-section {
  padding-top: 1.75rem;
  margin-top: 1.75rem;
  border-top: 1px solid var(--color-border);
}

.legal-section:first-of-type {
  padding-top: 0;
  margin-top: 0;
  border-top: 0;
}

.legal-section h2 {
  font-family: var(--font-sans);
  font-size: 1.05rem;
  font-weight: 600;
}

.legal-section p {
  margin-top: 0.7rem;
  font-family: var(--font-serif);
  font-size: 1rem;
  line-height: 1.9;
  color: var(--color-text-soft);
}
</style>
