import { useQuery } from '@tanstack/react-query'
import client from '@/api/client'

type Job = {
  id: string
  title: string
  company: string
  location?: string
}

export default function Jobs() {
  const { data } = useQuery({
    queryKey: ['jobs'],
    queryFn: async () => (await client.get('/jobs')).data,
  })

  const items: Job[] = data?.items ?? []

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">最新职位</h2>
      <ul className="space-y-2">
        {items.map((j) => (
          <li key={j.id} className="p-3 rounded border">
            <div className="font-medium">{j.title}</div>
            <div className="text-gray-500 text-sm">{j.company} · {j.location}</div>
          </li>
        ))}
      </ul>
    </div>
  )
}

