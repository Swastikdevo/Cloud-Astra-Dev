```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
    const [customers, setCustomers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState('');

    useEffect(() => {
        fetch('/api/customers')
            .then((response) => response.json())
            .then((data) => {
                setCustomers(data);
                setLoading(false);
            });
    }, []);

    const handleFilterChange = (e) => {
        setFilter(e.target.value);
    };

    const filteredCustomers = customers.filter(customer =>
        customer.name.toLowerCase().includes(filter.toLowerCase())
    );

    if (loading) return <p>Loading...</p>;

    return (
        <div>
            <input
                type="text"
                placeholder="Filter by name"
                value={filter}
                onChange={handleFilterChange}
            />
            <ul>
                {filteredCustomers.map((customer) => (
                    <li key={customer.id}>{customer.name}</li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerList;
```