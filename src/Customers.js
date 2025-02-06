```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
    const [customers, setCustomers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchCustomers = async () => {
            try {
                let response = await fetch('/api/customers');
                if (!response.ok) throw new Error('Network response was not ok');
                let data = await response.json();
                setCustomers(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };
        fetchCustomers();
    }, []);

    const toggleStatus = (id) => {
        setCustomers(customers.map(customer => customer.id === id ? { ...customer, active: !customer.active } : customer ));
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div>
            <h2>Customer List</h2>
            <ul>
                {customers.map(customer => (
                    <li key={customer.id}>
                        {customer.name} - {customer.active ? 'Active' : 'Inactive'}
                        <button onClick={() => toggleStatus(customer.id)}>Toggle Status</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerList;
```