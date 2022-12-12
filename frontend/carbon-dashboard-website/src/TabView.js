import Tab from 'react-bootstrap/Tab';
import Tabs from 'react-bootstrap/Tabs';
import CurrentUsage from './tabs/CurrentUsage';
import FutureAdvice from './tabs/FutureAdvice';
import PastUsage from './tabs/PastUsage';
import './TabView.css';

function TabView() {
    return (
        <div className="tabs">
            <Tabs
                defaultActiveKey="pastUsage"
                id="tab-view"
                className="m-3"
            >
                <Tab eventKey="pastUsage" title="Past Usage">
                    <PastUsage />
                </Tab>
                <Tab eventKey="currentUsage" title="Current Usage">
                    <CurrentUsage />
                </Tab>
                <Tab eventKey="futureAdvice" title="Future Advice">
                    <FutureAdvice />
                </Tab>
            </Tabs>
        </div>
    );
}

export default TabView;