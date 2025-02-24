```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
    const [customers, setCustomers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchCustomers = async () => {
            try {
                const response = await fetch('/api/customers');
                if (!response.ok) throw new Error('Network response was not ok');
                const data = await response.json();
                setCustomers(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };
        fetchCustomers();
    }, []);

    const handleRemoveCustomer = async (id) => {
        setCustomers(customers.filter(customer => customer.id !== id));
        await fetch(`/api/customers/${id}`, { method: 'DELETE' });
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div>
            <h1>Customer List</h1>
            <ul>
                {customers.map(customer => (
                    <li key={customer.id}>
                        {customer.name} 
                        <button onClick={() => handleRemoveCustomer(customer.id)}>Remove</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerList;
```