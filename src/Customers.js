```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
    const [customers, setCustomers] = useState([]);
    const [filter, setFilter] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('/api/customers')
            .then(response => response.json())
            .then(data => {
                setCustomers(data);
                setLoading(false);
            });
    }, []);

    const filteredCustomers = customers.filter(customer => 
        customer.name.toLowerCase().includes(filter.toLowerCase())
    );

    const handleFilterChange = (e) => setFilter(e.target.value);

    if (loading) return <div>Loading...</div>;

    return (
        <div>
            <input 
                type="text" 
                placeholder="Search customers..." 
                value={filter} 
                onChange={handleFilterChange} 
            />
            <ul>
                {filteredCustomers.map(customer => (
                    <li key={customer.id}>{customer.name} - {customer.email}</li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerList;
```