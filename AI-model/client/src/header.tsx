import {Link} from "react-router-dom";
import './header.css'
import logo from './assets/chalmers-university-of-technology-logo-png_seeklogo-28934.png'

function Header(){
    return(
        <nav className='header d-flex'>
            <Link to='/' ><img src={logo} className='logo-chalmers' alt='Home button'/></Link>
            <div className='nav-content justify-content-center'>
                <ul className='nav-list d-flex justify-content-center'>
                    <li><Link to="/" style={{ textDecoration: 'none' }}>Home</Link></li>
                    <li><Link to="/Data" style={{ textDecoration: 'none' }}>Data</Link></li>
                    <li><Link to="/About us" style={{ textDecoration: 'none' }} >About us</Link></li>
                </ul>
            </div>
        </nav>
    )

}
export default Header;