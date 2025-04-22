import Header from './header';
import {useState} from "react";
import './mainpage.css'
import arrowIcon from './assets/arrow 1 (1).png';

function Mainpage(){
    const [question,setQuestion] = useState('');
    const [answer,setAnswer] = useState('');
    const [list , setlist] = useState(['']);

    function Promptlist(){
        const displayList = []
        displayList.push(question);
        displayList.push(answer);
        setlist(displayList);
    }

    //Make question and answer two separate fields (components). These are then added to a list when a button is pressed and later displayed.
    return(
            <div>
                <Header/>
                <div className='answer-area'>
                    <ul>
                        {list.map( (item,index)  => (<li key={index}>{item}</li>))}
                    </ul>
                </div>
                <div className='d-flex justify-content-center '>
                    <input className='input-bar' placeholder='Write your question here!' value={question} onChange={(e) => setQuestion(e.target.value)}/>
                    <button className='prompt-button' onClick={Promptlist}><img className='arrow' src={arrowIcon} alt='submit answer button'/></button>
                </div>
            </div>


    )
}
export default Mainpage;