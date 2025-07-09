```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
    const [customers, setCustomers] = useState([]);
    const [error, setError] = useState(null);
    
    useEffect(() => {
        fetch('https://api.example.com/customers')
            .then(response => response.json())
            .then(data => setCustomers(data))
            .catch(error => setError(error));
    }, []);

    const removeCustomer = (id) => {
        setCustomers(customers.filter(customer => customer.id !== id));
    };

    if (error) return <div>Error loading customers</div>;
    
    return (
        <div>
            <h1>Customer List</h1>
            <ul>
                {customers.map(customer => (
                    <li key={customer.id}>
                        {customer.name}
                        <button onClick={() => removeCustomer(customer.id)}>Remove</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerList;
```