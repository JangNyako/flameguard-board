'use client'

import { useEffect, useState } from 'react'
import './alarm.css'

type AlarmItem = {
  message: string
  created_at: string
  result_image?: string
}

export default function AlarmPage() {
  const [alarms, setAlarms] = useState<AlarmItem[]>([])

  useEffect(() => {
    fetch('http://localhost:8000/api/alarm/list')
      .then(res => res.json())
      .then(data => {
        const filtered = data.filter(
          (item: AlarmItem) => item.message.toLowerCase() !== 'safe',
        )
        setAlarms(filtered)
      })
      .catch(err => console.error('알림 가져오기 실패:', err))
  }, [])

  return (
    <main className="container">
      <h1>알림 목록</h1>

      <div className="section">
        {alarms.length === 0 ? (
          <p>표시할 알림이 없습니다.</p>
        ) : (
          <ol>
            {alarms.map((item, index) => (
              <li key={index} className="notice">
                [{item.message}] ({item.created_at})
                {item.result_image && (
                  <div>
                    <img
                      src={`http://localhost:8000/log/${item.result_image}`}
                      alt="감지 이미지"
                      width={200}
                      onError={e => {
                        console.error('이미지 로딩 실패:', e.currentTarget.src)
                      }}
                    />
                  </div>
                )}
              </li>
            ))}
          </ol>
        )}
      </div>

      <button onClick={() => (window.location.href = '/mainboard')}>
        돌아가기
      </button>
    </main>
  )
}
