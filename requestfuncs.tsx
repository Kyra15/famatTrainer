import { useEffect, useState } from 'react'

const fetchFromApi = async () => {
    const response = await fetch('http://localhost:3001/api/question', {
        headers: { 'Content-Type': 'application/json' },
    })
    if (response.ok) return response.json()
    else return { status: response.status }
}

export default function RequestDemo() {
    const [response, setResponse] = useState(null)

    useEffect(() => {
        fetchFromApi().then(setResponse)
    }, [])

    if (!response) return <div>Loading...</div>
    return <pre>{JSON.stringify(response, null, 2)}</pre>
}