import {Link} from "react-router-dom";
import './header.css'
import logo from './assets/chalmers-university-of-technology-logo-png_seeklogo-28934.png'

function Header(){
    return(
        <nav className='header d-flex'>
            <Link to='/' ><img src={logo} className='logo-chalmers' alt='Home button'/></Link>
            <div className='nav-content justify-content-center'>
                <ul className='nav-list d-flex justify-content-center' >
                    <li className='list-item'><Link to="/" style={{ textDecoration: 'none' , color:"white" }}>Home</Link></li>
                    <li className='list-item'><Link to="/Data" style={{ textDecoration: 'none' , color:"white" }}>Data</Link></li>
                    <li className='list-item'><Link to="/About us" style= {{ textDecoration: 'none' , color:"white" }} >About us</Link></li>
                </ul>
            </div>
        </nav>
    )

}
export default Header;