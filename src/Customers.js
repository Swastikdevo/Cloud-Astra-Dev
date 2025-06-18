```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
    const [customers, setCustomers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch('/api/customers')
            .then(response => response.json())
            .then(data => {
                setCustomers(data);
                setLoading(false);
            })
            .catch(err => {
                setError(err);
                setLoading(false);
            });
    }, []);

    const handleDelete = (id) => {
        fetch(`/api/customers/${id}`, { method: 'DELETE' })
            .then(() => setCustomers(customers.filter(customer => customer.id !== id)))
            .catch(err => setError(err));
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error loading customers</div>;

    return (
        <div>
            <h2>Customer List</h2>
            <ul>
                {customers.map(customer => (
                    <li key={customer.id}>
                        {customer.name} <button onClick={() => handleDelete(customer.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerList;
```