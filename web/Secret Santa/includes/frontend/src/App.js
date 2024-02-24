import Home from "./home"
import Secure from "./secure"
import {BrowserRouter as Router, Route, Switch} from 'react-router-dom'


function App() {
  return (
    <Router>
        <div className="content">
          <Switch>
            <Route exact path='/'>
                <Secure />
            </Route>
            <Route exact path='/pragyan'>
                <Home />
            </Route>
            {/* <Route path='/secure'>
              <Create />
            </Route> */}
          </Switch>
        </div>
      
    </Router>
  );
}

export default App;
