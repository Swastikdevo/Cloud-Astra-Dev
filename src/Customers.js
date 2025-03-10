```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
    const [customers, setCustomers] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [sortOrder, setSortOrder] = useState('asc');

    useEffect(() => {
        fetch('/api/customers')
            .then(response => response.json())
            .then(data => setCustomers(data));
    }, []);

    const filteredCustomers = customers.filter(customer => 
        customer.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const sortedCustomers = filteredCustomers.sort((a, b) => {
        const comparison = a.name.localeCompare(b.name);
        return sortOrder === 'asc' ? comparison : -comparison;
    });

    const handleSortToggle = () => {
        setSortOrder(order => (order === 'asc' ? 'desc' : 'asc'));
    };

    return (
        <div>
            <input 
                type="text" 
                placeholder="Search customers..." 
                value={searchTerm} 
                onChange={e => setSearchTerm(e.target.value)} 
            />
            <button onClick={handleSortToggle}>
                Sort {sortOrder === 'asc' ? 'Descending' : 'Ascending'}
            </button>
            <ul>
                {sortedCustomers.map(customer => (
                    <li key={customer.id}>{customer.name} - {customer.email}</li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerList;
```