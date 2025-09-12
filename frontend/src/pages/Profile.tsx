import { useQuery } from '@tanstack/react-query'
import client from '@/api/client'

export default function Profile() {
  const { data } = useQuery({ queryKey: ['me'], queryFn: async () => (await client.get('/users/me')).data })
  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">个人信息</h2>
      <pre className="p-3 bg-gray-50 border rounded">{JSON.stringify(data, null, 2)}</pre>
    </div>
  )
}

