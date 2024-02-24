import Pickle from "./pickle"
import {BrowserRouter as Router, Route, Switch} from 'react-router-dom'


function App() {
  return (
    <Router>
        <div className="content">
          <Switch>
            <Route exact path='/'>
                <Pickle />
            </Route>
          </Switch>
        </div>
      
    </Router>
  );
}

export default App;