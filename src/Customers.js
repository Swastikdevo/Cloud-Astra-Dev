```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
    const [customers, setCustomers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [sortOrder, setSortOrder] = useState('asc');

    useEffect(() => {
        fetch('/api/customers')
            .then(response => response.json())
            .then(data => {
                setCustomers(data);
                setLoading(false);
            });
    }, []);

    const sortCustomers = () => {
        const sortedCustomers = [...customers].sort((a, b) => {
            return sortOrder === 'asc' 
                ? a.name.localeCompare(b.name) 
                : b.name.localeCompare(a.name);
        });
        setCustomers(sortedCustomers);
        setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    };

    if (loading) return <div>Loading...</div>;

    return (
        <div>
            <h1>Customer List</h1>
            <button onClick={sortCustomers}>
                Sort by Name: {sortOrder === 'asc' ? 'Descending' : 'Ascending'}
            </button>
            <ul>
                {customers.map((customer) => (
                    <li key={customer.id}>{customer.name}</li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerList;
```