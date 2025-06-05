```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
    const [customers, setCustomers] = useState([]);
    const [filter, setFilter] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchCustomers = async () => {
            const res = await fetch('/api/customers');
            const data = await res.json();
            setCustomers(data);
            setLoading(false);
        };
        fetchCustomers();
    }, []);

    const filteredCustomers = customers.filter(customer => 
        customer.name.toLowerCase().includes(filter.toLowerCase())
    );

    const handleDelete = async (id) => {
        await fetch(`/api/customers/${id}`, { method: 'DELETE' });
        setCustomers(customers.filter(customer => customer.id !== id));
    };

    if (loading) return <div>Loading...</div>;

    return (
        <div>
            <input 
                type="text" 
                value={filter} 
                onChange={(e) => setFilter(e.target.value)} 
                placeholder="Search customers" 
            />
            <ul>
                {filteredCustomers.map(customer => (
                    <li key={customer.id}>
                        {customer.name} 
                        <button onClick={() => handleDelete(customer.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerList;
```