import { useState } from 'react'
import client from '@/api/client'

export default function Resume() {
  const [file, setFile] = useState<File | null>(null)

  const upload = async () => {
    if (!file) return
    const form = new FormData()
    form.append('file', file)
    await client.post('/resumes/upload', form, { headers: { 'Content-Type': 'multipart/form-data' } })
    alert('上传成功')
  }

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">上传简历</h2>
      <input type="file" onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
      <button className="ml-2 px-3 py-1 rounded bg-blue-600 text-white" onClick={upload}>上传</button>
    </div>
  )
}

