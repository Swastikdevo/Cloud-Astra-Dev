```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchCustomers();
    }, []);

    const fetchCustomers = async () => {
        setLoading(true);
        const response = await fetch('/api/customers');
        const data = await response.json();
        setCustomers(data);
        setLoading(false);
    };

    const deleteCustomer = async (id) => {
        await fetch(`/api/customers/${id}`, { method: 'DELETE' });
        setCustomers(customers.filter(customer => customer.id !== id));
    };

    return (
        <div>
            <h1>Customer Management</h1>
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

export default CustomerManagement;
```