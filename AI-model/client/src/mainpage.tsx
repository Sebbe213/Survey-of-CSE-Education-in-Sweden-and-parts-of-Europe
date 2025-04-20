import Header from './header';
import {useState} from "react";

function Mainpage(){
    const [question,setQuestion] = useState('');
    const [answer,setAnswer] = useState('');
    return(
            <div>
                <Header/>
                <div>
                    <p>{question}</p>
                    <p>{answer}</p>
                </div>

                <></>
            </div>


    )
}
export default Mainpage;