```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
    const [customers, setCustomers] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('/api/customers')
            .then(response => response.json())
            .then(data => {
                setCustomers(data);
                setLoading(false);
            });
    }, []);

    const deleteCustomer = (id) => {
        fetch(`/api/customers/${id}`, { method: 'DELETE' })
            .then(() => {
                setCustomers(customers.filter(customer => customer.id !== id));
            });
    };

    return (
        <div>
            {loading ? <p>Loading...</p> : (
                <ul>
                    {customers.map(customer => (
                        <li key={customer.id}>
                            {customer.name}
                            <button onClick={() => deleteCustomer(customer.id)}>Delete</button>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default CustomerList;
```