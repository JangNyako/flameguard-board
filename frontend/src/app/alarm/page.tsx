import './alarm.css' // alarm.css는 동일 폴더에 있어야 함

export default function AlarmPage() {
  return (
    <main className="container">
      <h1>알림 목록</h1>

      <div className="section">
        <h2>알림 항목</h2>
        <ol>
          <li className="notice">[화재 감지] (2025-03-24 13:40)</li>
          <li className="report">[화재 감지] (2025-03-22 09:15)</li>
          <li className="check">[연기 감지] (2025-03-20 17:30)</li>
        </ol>
      </div>

      <button onClick={() => (window.location.href = '/mainboard')}>
        돌아가기
      </button>
    </main>
  )
}
