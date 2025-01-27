```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
    const [customers, setCustomers] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('/api/customers')
            .then(res => res.json())
            .then(data => {
                setCustomers(data);
                setLoading(false);
            });
    }, []);

    const deleteCustomer = (id) => {
        fetch(`/api/customers/${id}`, { method: 'DELETE' })
            .then(() => setCustomers(customers.filter(customer => customer.id !== id)));
    };

    if (loading) return <div>Loading...</div>;

    return (
        <ul>
            {customers.map(customer => (
                <li key={customer.id}>
                    {customer.name}
                    <button onClick={() => deleteCustomer(customer.id)}>Delete</button>
                </li>
            ))}
        </ul>
    );
};

export default CustomerList;
```