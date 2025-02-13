```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
    const [customers, setCustomers] = useState([]);
    const [filterText, setFilterText] = useState('');

    useEffect(() => {
        fetch('/api/customers')
            .then(response => response.json())
            .then(data => setCustomers(data))
            .catch(error => console.error('Error fetching customers:', error));
    }, []);

    const filteredCustomers = customers.filter(customer => 
        customer.name.toLowerCase().includes(filterText.toLowerCase())
    );

    return (
        <div>
            <input 
                type="text" 
                placeholder="Filter customers" 
                value={filterText} 
                onChange={e => setFilterText(e.target.value)} 
            />
            <ul>
                {filteredCustomers.map(customer => (
                    <li key={customer.id}>
                        {customer.name} - {customer.email}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerList;
```