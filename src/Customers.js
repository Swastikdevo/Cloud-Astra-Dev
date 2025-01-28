```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
    const [customers, setCustomers] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchCustomers = async () => {
            const response = await fetch('/api/customers');
            const data = await response.json();
            setCustomers(data);
            setLoading(false);
        };
        fetchCustomers();
    }, []);

    const toggleStatus = (id) => {
        setCustomers(customers.map(customer => 
            customer.id === id ? { ...customer, active: !customer.active } : customer));
    };

    return (
        <div>
            <h1>Customer List</h1>
            {loading ? <p>Loading...</p> : (
                <ul>
                    {customers.map(customer => (
                        <li key={customer.id}>
                            {customer.name} - {customer.active ? 'Active' : 'Inactive'}
                            <button onClick={() => toggleStatus(customer.id)}>
                                Toggle Status
                            </button>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default CustomerList;
```