import './question.css'



function Questionmodal({ question }: { question: string | undefined }) {
    return (
        <div className='questionmodal  align-items-center'>
            <p className='question'>{question}</p>
        </div>

    )
}

export default Questionmodal;