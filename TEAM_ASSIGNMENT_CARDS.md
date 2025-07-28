# Team Assignment Cards - Quick Reference

---

## 🎯 **TEAM MEMBER 1: User Management & Authentication**

### **Your Assignment:**
- **2 Models**: UserProfile, Category
- **2 Forms**: CustomUserCreationForm, UserProfileForm  
- **2 Views**: UserProfileView, IndexView

### **Key Files to Work On:**
- `models.py`: UserProfile, Category classes
- `forms.py`: CustomUserCreationForm, UserProfileForm classes
- `views.py`: user_profile_view, IndexView class
- `urls.py`: Profile and index URL patterns

### **Your Focus:**
✅ User registration and login system  
✅ Profile management with avatars  
✅ Category management system  
✅ Homepage with featured content  
✅ User session tracking  

---

## 🎯 **TEAM MEMBER 2: Content Management & Ideas**

### **Your Assignment:**
- **2 Models**: GreenIdea, Comment
- **2 Forms**: GreenIdeaForm, CommentForm
- **2 Views**: IdeaDetailView, AddCommentView

### **Key Files to Work On:**
- `models.py`: GreenIdea, Comment classes
- `forms.py`: GreenIdeaForm, CommentForm classes
- `views.py`: IdeaDetailView class, add_comment_view function
- `urls.py`: Idea detail and comment URL patterns

### **Your Focus:**
✅ Idea submission and editing  
✅ Comment system implementation  
✅ Idea detail pages with interactions  
✅ Content moderation system  
✅ Image upload for ideas  

---

## 🎯 **TEAM MEMBER 3: Community Engagement & Ratings**

### **Your Assignment:**
- **2 Models**: Rating, Event
- **2 Forms**: RatingForm, EventForm
- **2 Views**: AddRatingView, EventListView

### **Key Files to Work On:**
- `models.py`: Rating, Event classes
- `forms.py`: RatingForm, EventForm classes
- `views.py`: add_rating_view, EventListView class
- `urls.py`: Rating and event URL patterns

### **Your Focus:**
✅ 1-5 star rating system  
✅ Event creation and management  
✅ User engagement features  
✅ Event listing with filters  
✅ Online/offline event support  

---

## 🎯 **TEAM MEMBER 4: Project Management & Collaboration**

### **Your Assignment:**
- **2 Models**: Project, Collaboration
- **2 Forms**: ProjectForm, CollaborationForm
- **2 Views**: ProjectListView, CollaborationRequestView

### **Key Files to Work On:**
- `models.py`: Project, Collaboration classes
- `forms.py`: ProjectForm, CollaborationForm classes
- `views.py`: ProjectListView class, collaboration_request_view function
- `urls.py`: Project and collaboration URL patterns

### **Your Focus:**
✅ Project creation and management  
✅ Collaboration request workflow  
✅ Project status tracking  
✅ Team coordination features  
✅ Role-based permissions  

---

## 🎯 **TEAM MEMBER 5: Resource Sharing & Communication**

### **Your Assignment:**
- **2 Models**: Resource, Newsletter
- **2 Forms**: ResourceForm, NewsletterForm
- **2 Views**: ResourceListView, NewsletterListView

### **Key Files to Work On:**
- `models.py`: Resource, Newsletter classes
- `forms.py`: ResourceForm, NewsletterForm classes
- `views.py`: ResourceListView, NewsletterListView classes
- `urls.py`: Resource and newsletter URL patterns

### **Your Focus:**
✅ Resource upload and management  
✅ Newsletter publishing system  
✅ File sharing with download tracking  
✅ Staff-only features  
✅ Content organization by type  

---

## 📋 **SHARED RESPONSIBILITIES**

### **All Team Members Must:**
- ✅ Coordinate URL patterns to avoid conflicts
- ✅ Test integration with other team features
- ✅ Follow consistent coding standards
- ✅ Update documentation for their features
- ✅ Participate in code reviews

### **Integration Points:**
- 🔗 **Authentication**: All features need user login
- 🔗 **Categories**: Used across multiple features
- 🔗 **File Uploads**: Shared upload system
- 🔗 **Search**: Cross-feature search functionality

---

## 🚀 **GETTING STARTED**

### **Step 1: Setup**
```bash
cd DjangoFinal
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### **Step 2: Focus on Your Assignment**
- Review your assigned models, forms, and views
- Understand the relationships between your components
- Plan your implementation approach

### **Step 3: Development**
- Implement your models first
- Create your forms with proper validation
- Build your views with templates
- Test your functionality thoroughly

### **Step 4: Integration**
- Coordinate with other team members
- Test cross-feature functionality
- Ensure URL patterns don't conflict
- Document your implementation

---

## 📞 **COMMUNICATION**

### **Daily Check-ins:**
- Progress updates
- Blockers and dependencies
- Integration questions
- Code review requests

### **Weekly Reviews:**
- Feature demonstrations
- Integration testing
- Timeline updates
- Quality assurance

### **Final Integration:**
- Cross-team testing
- Bug fixes
- Performance optimization
- Documentation completion 