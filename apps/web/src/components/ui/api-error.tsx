

export default function ApiError({ error }) {
  return (
    <div className="text-red-500">
      {error?.message}
    </div>
  )
}