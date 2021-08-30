const profileImg = document.querySelector('.profile-img');
const profileCard = document.querySelector('.profile-card');

if (profileImg) {
  profileImg.addEventListener('click', () => {
    if (profileCard.style.display === 'block') {
      profileCard.style.display = 'none';
    } else {
      profileCard.style.display = 'block';
    }
  });
}

document.addEventListener('mousedown', (e) => {
  if (!profileImg.contains(e.target) && !profileCard.contains(e.target)) {
    profileCard.style.display = 'none';
  }
});

