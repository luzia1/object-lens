import './App.css'
import { Header } from './components/layout/Header'
import { HeroSection } from './components/layout/HeroSection'
import { ImageUploader } from './components/layout/ImageUploader'

function App() {

  return (
    <div className='min-h-screen bg-background text-foreground'>
      <Header/>
      <main className='mx-auto max-w-5xl px-6 py-12'>
        <HeroSection/>
        <ImageUploader/>
      </main>
    </div>
  )
}

export default App
