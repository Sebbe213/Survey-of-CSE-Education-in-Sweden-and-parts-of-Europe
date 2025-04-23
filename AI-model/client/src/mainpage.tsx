import Header from './header';
import {useState} from "react";
import './mainpage.css'
import Questionmodal from './question'
import arrowIcon from './assets/arrow 1 (1).png';
//TODO:
//      - Fix the header so that it has a border
//      - Fix the input bar so that it looks better
//       - Fix the answer box so that it looks better
function Mainpage() {
    const [question, setQuestion] = useState<string>();
    const [answer, setAnswer] = useState<string>();
    const [list, setlist] = useState<{ question: JSX.Element; answer: JSX.Element }[]>([]);

    function Promptlist() {
        setlist((prevList: any) => [...prevList,
            {question: <Questionmodal question={question}/>, answer: <p className='answer'>Answer: {answer}</p>}])
        setQuestion('')

    }
    function Getanswerbutton(){
        if(question === undefined || question === ''){
            return(<button className='prompt-button' ><img className='arrow' src={arrowIcon} alt='submit answer button'/></button>)
        }
        return(
            <button className='prompt-button' onClick={Promptlist}><img className='arrow' src={arrowIcon} alt='submit answer button'/></button>
        )
    }
    return (
        <body>
        <Header/>
            <div className='answer-area  justify-content-center align-items-center'>
                <ul style={{listStyle: 'none'}}>
                    {list.map((item,index)  => (<li key={index}> {item.question}
                        {item.answer} <hr/> </li> ))}
                    </ul>
                </div>
                <div className='d-flex justify-content-center '>
                    <input className='input-bar' placeholder='Write your question here!' value={question} onChange={(e) => setQuestion(e.target.value) }/>
                    <Getanswerbutton/>
                </div>
        </body>




    )
}
export default Mainpage;