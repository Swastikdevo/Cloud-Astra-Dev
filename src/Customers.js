```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
    const [customers, setCustomers] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        fetch('/api/customers')
            .then(response => response.json())
            .then(data => {
                setCustomers(data);
                setIsLoading(false);
            });
    }, []);

    const deleteCustomer = (id) => {
        setCustomers(customers.filter(customer => customer.id !== id));
    };

    if (isLoading) return <div>Loading...</div>;

    return (
        <div>
            <h1>Customer List</h1>
            <ul>
                {customers.map(customer => (
                    <li key={customer.id}>
                        {customer.name} 
                        <button onClick={() => deleteCustomer(customer.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerList;
```