import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'

type AnalysisResult = {
    filename: string,
    content_type: string,
    size: number
}

export function ImageUploader() {

    const [image, setImage] = useState<string | null>(null)
    const [selectedFile, setSelectedFile] = useState<File | null>(null)
    const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null)
    const [isLoading, setIsLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        return () => {
            if (image) {
                URL.revokeObjectURL(image)
            }
        }
    }, [image])

    const prepareImageData = () => {
        if (!selectedFile) return

        const formData = new FormData()
        formData.append('image', selectedFile)

        return formData
    }

    
    const analyzeImage = async () => {
        const formData = prepareImageData()

        if (!formData) return

        setIsLoading(true)
        setError(null)

        try{
            const response = await fetch(
                'http://127.0.0.1:8000/images/analyze',
                {
                    method: 'POST',
                    body: formData
                }
            )

            if(!response.ok){
                throw new Error('Não foi possivel analisar a imagem.')
            }

            const data = await response.json()

            setAnalysisResult(data)

        } catch (error){
            setError(error instanceof Error ? error.message : 'Ocorreu um erro inesperado.')

        } finally{
            setIsLoading(false)
        }
    }

    return (
        <section className="mt-10 space-y-4">
            <div>
                <h3 className="text-lg font-medium">
                    Carrega uma imagem para começar
                </h3>

                <p className="mt-1 text-sm text-gray-500">
                    Seleciona uma imagem do teu computador para analisar as suas cores.
                </p>
            </div>

            <label htmlFor="image-upload" className="flex cursor-pointer flex-col items-center justify-center gap-3 rounded-xl border-2 border-dashed border-gray-300 px-6 py-12 text-center transition-colors hover:border-gray-500 hover:bg-gray-50">
                <p className="font-medium text-gray-700">
                    Selecionar imagem
                </p>
                <p className="text-sm text-gray-500">
                    PNG, JPG ou JPEG
                </p>
                <input id="image-upload" type="file" accept="image/png, image/jpeg" className="sr-only"
                    onChange={(event) => {
                        const file = event.target.files?.[0]

                        if (file) {
                            setImage(URL.createObjectURL(file))
                            setSelectedFile(file)
                        }

                        event.currentTarget.value = ''
                    }}
                />

                {image && (
                    <div className='mt-4 space-y-3'>
                        <img src={image} alt="Imagem selecionada" className="h-80 w-full rounded-lg object-contain" />
                        <Button className='text-sm bg-red-800 hover:bg-red-500'
                            onClick={() => {
                                setImage(null)
                                setSelectedFile(null)
                                setAnalysisResult(null)
                                setError(null)
                            }}>
                            Remover imagem
                        </Button>
                        <Button 
                            onClick={analyzeImage}
                            disabled={isLoading}
                            >
                                {isLoading ? 'A analisar...' : 'Analisar imagem'}
                        </Button>
                    </div>
                )}

                {analysisResult && (
                    <div className="mt-4 rounded-lg border p-4 space-y-2">
                        <h4 className="font-medium">Resultado da análise</h4>

                        <p>Ficheiro: {analysisResult.filename}</p>
                        <p>Formato: {analysisResult.content_type}</p>
                        <p>Tamanho: {analysisResult.size} bytes</p>
                    </div>
                )}

                {error && (
                    <p className="text-sm text-red-600">
                        {error}
                    </p>
                )}

            </label>
        </section>
    )
}